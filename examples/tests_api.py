import requests
import pytest


"""
API-тесты (pytest + requests)
"""

BASE_URL = "https://petstore.swagger.io/v2"

# 1. GET и статус
def test_get_pet_by_id():
    r = requests.get(f"{BASE_URL}/pet/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1

# 2. POST
def test_create_pet():
    payload = {"id": 12345, "name": "Rex", "status": "available"}
    r = requests.post(f"{BASE_URL}/pet", json=payload)
    assert r.status_code == 200
    assert r.json()["name"] == "Rex"

# 3. Negative (404)
def test_pet_not_found():
    r = requests.get(f"{BASE_URL}/pet/99999999")
    assert r.status_code == 404

# 4. Проверка массива (сортировка)
def test_pets_sorted_by_id():
    # petstore не возвращает массив — пример условный:
    pets = [{"id": 1}, {"id": 2}, {"id": 3}]
    ids = [p["id"] for p in pets]
    assert ids == sorted(ids)

# 5. Contract validation (pydantic)
from pydantic import BaseModel
class Pet(BaseModel):
    id: int
    name: str
    status: str

def test_pet_contract():
    r = requests.get(f"{BASE_URL}/pet/1")
    pet = Pet(**r.json())  # валидация по схеме
    assert pet.status in {"available", "pending", "sold"}
