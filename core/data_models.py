from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class Category(BaseModel):
    id: Optional[int] = Field(default=None, ge=0) # означает “число ≥ 0, можно не передавать (или передать null)”.
    name: Optional[str] = None


class Tag(BaseModel):
    id: Optional[int] = Field(default=None, ge=0)
    name: Optional[str] = None


class PetStatus(str, Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


class Pet(BaseModel):
    id: Optional[int] = Field(default=None, ge=0)
    category: Optional[Category] = None
    name: str
    photoUrls: List[str]
    tags: Optional[List[Tag]] = None
    status: Optional[PetStatus] = None
