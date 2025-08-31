from __future__ import annotations

from fastapi import FastAPI, HTTPException, Depends, Header, status, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List, Dict
from datetime import datetime
import itertools
import time
import json

"""
Run the service:
pip install "fastapi[standard]" uvicorn
uvicorn main:app --reload --port 8001

Swagger docs:
http://127.0.0.1:8001/docs#/
"""

app = FastAPI(title="Mini API for Testing", version="1.0.0")

# -----------------------
# Auth (very simple)
# -----------------------
TEST_USER = {"username": "test", "password": "test"}
VALID_TOKENS: set[str] = set()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"


def get_current_user(authorization: str = Header(default="")) -> str:
    """Expect Authorization: Bearer <token>"""
    if authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
        if token in VALID_TOKENS:
            return TEST_USER["username"]
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid or missing token",
                        headers={"WWW-Authenticate": "Bearer"})


@app.post("/auth/login", response_model=LoginResponse, tags=["auth"])
def login(req: LoginRequest):
    if req.username == TEST_USER["username"] and req.password == TEST_USER["password"]:
        token = "test-token"
        VALID_TOKENS.add(token)
        return LoginResponse(access_token=token)
    raise HTTPException(status_code=401, detail="Bad credentials")

# -----------------------
# Pet resource (CRUD)
# -----------------------
class PetStatus(str, Enum):
    available = "available"
    pending = "pending"
    sold = "sold"

class Category(BaseModel):
    id: Optional[int] = Field(default=None, ge=0)
    name: Optional[str] = None

class Tag(BaseModel):
    id: Optional[int] = Field(default=None, ge=0)
    name: Optional[str] = None

class PetBase(BaseModel):
    name: str = Field(..., min_length=1)
    status: PetStatus = PetStatus.available
    category: Optional[Category] = None
    photoUrls: List[str] = Field(default_factory=list)
    tags: Optional[List[Tag]] = None

class PetCreate(PetBase):
    pass

class PetUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    status: Optional[PetStatus] = None
    category: Optional[Category] = None
    photoUrls: Optional[List[str]] = None
    tags: Optional[List[Tag]] = None

class Pet(PetBase):
    id: int
    created_at: datetime
    version: int = 1


# In-memory DB
_id_counter = itertools.count(1)
PETS: Dict[int, Pet] = {}
# Idempotency store: key -> {"body": str, "pet_id": int}
IDEMP_STORE: Dict[str, Dict[str, str | int]] = {}


def _canonical_body(model: BaseModel) -> str:
    # stable JSON for idempotency comparison
    return json.dumps(model.model_dump(), sort_keys=True, separators=(",", ":"))


def _pet_to_response(pet: Pet) -> JSONResponse:
    # Attach ETag (weak) as version
    headers = {"ETag": f'W/"{pet.version}"'}
    return JSONResponse(content=pet.model_dump(), headers=headers)


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.post("/pets", response_model=Pet, status_code=201, tags=["pets"])
def create_pet(req: PetCreate,
               idempotency_key: Optional[str] = Header(default=None, alias="Idempotency-Key"),
               user: str = Depends(get_current_user)):
    # Handle idempotency
    if idempotency_key:
        entry = IDEMP_STORE.get(idempotency_key)
        body = _canonical_body(req)
        if entry:
            if entry["body"] == body:
                # Return existing resource (200 OK) with replay header
                pet = PETS.get(int(entry["pet_id"]))
                if not pet:
                    # stale entry, treat as new
                    pass
                else:
                    resp = _pet_to_response(pet)
                    resp.status_code = 200
                    resp.headers["Idempotency-Replayed"] = "true"
                    return resp
            else:
                raise HTTPException(status_code=409, detail="Idempotency-Key already used with different body")

    pet_id = next(_id_counter)
    pet = Pet(id=pet_id, created_at=datetime.utcnow(), **req.model_dump())
    PETS[pet_id] = pet

    if idempotency_key:
        IDEMP_STORE[idempotency_key] = {"body": _canonical_body(req), "pet_id": pet_id}

    return _pet_to_response(pet)


@app.get("/pets/{pet_id}", response_model=Pet, tags=["pets"])
def get_pet(pet_id: int):
    pet = PETS.get(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return _pet_to_response(pet)


@app.get("/pets", tags=["pets"])
def list_pets(status: Optional[PetStatus] = Query(default=None),
              limit: int = Query(default=10, ge=1, le=100),
              cursor: Optional[int] = Query(default=None, description="Return items with id > cursor")):
    items = [p for p in PETS.values() if status is None or p.status == status]
    items.sort(key=lambda p: p.id)
    if cursor:
        items = [p for p in items if p.id > cursor]
    page = items[:limit]
    next_cursor = page[-1].id if len(page) == limit else None
    return {
        "data": [p.model_dump() for p in page],
        "next": next_cursor
    }


@app.put("/pets/{pet_id}", response_model=Pet, tags=["pets"])
def replace_pet(pet_id: int,
                req: PetCreate,
                if_match: Optional[str] = Header(default=None, alias="If-Match"),
                user: str = Depends(get_current_user)):
    pet = PETS.get(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    # Optimistic concurrency via If-Match: expect version number
    if if_match is not None:
        try:
            expected = int(if_match.strip('W/"'))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid If-Match header")
        if expected != pet.version:
            raise HTTPException(status_code=412, detail="Version mismatch")

    pet = Pet(id=pet_id, created_at=pet.created_at, version=pet.version + 1, **req.model_dump())
    PETS[pet_id] = pet
    return _pet_to_response(pet)


@app.patch("/pets/{pet_id}", response_model=Pet, tags=["pets"])
def update_pet(pet_id: int,
               req: PetUpdate,
               if_match: Optional[str] = Header(default=None, alias="If-Match"),
               user: str = Depends(get_current_user)):
    pet = PETS.get(pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    if if_match is not None:
        try:
            expected = int(if_match.strip('W/"'))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid If-Match header")
        if expected != pet.version:
            raise HTTPException(status_code=412, detail="Version mismatch")

    data = pet.model_dump()
    patch = req.model_dump(exclude_unset=True)
    data.update(patch)
    pet = Pet(**data, version=pet.version + 1)
    PETS[pet_id] = pet
    return _pet_to_response(pet)


@app.delete("/pets/{pet_id}", status_code=204, tags=["pets"])
def delete_pet(pet_id: int, user: str = Depends(get_current_user)):
    if pet_id not in PETS:
        raise HTTPException(status_code=404, detail="Pet not found")
    PETS.pop(pet_id)
    return JSONResponse(status_code=204, content=None)


# Utilities for testing timeouts
@app.get("/slow", tags=["meta"])
def slow(delay: float = Query(1.0, ge=0.0, le=10.0)):
    time.sleep(delay)
    return {"slept": delay}


# Root doc
@app.get("/", tags=["meta"])
def root():
    return {"message": "Mini API for testing. See /docs for Swagger UI."}
