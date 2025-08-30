from uuid import uuid4

import pytest
import requests

from core.config import Config
from core.api.data_models import Category, Pet
from helpers.api_assertions import verify_ok_response

new_pet_data = Pet(
    category=Category(id=1, name="home"),
    name=f"kitty_{uuid4().hex[:8]}",
    photoUrls=["photo_url"],
    status="available")

@pytest.fixture
def new_pet(pet_api: Pet):
     response = requests.post(Config.BASE_PET_STORE_URL, new_pet_data)
     response.raise_for_status()
     pet_response = Pet(**response.json()) #** - deserialization
     # sleep(5)
     yield pet_response #for shearing to every test

     pet_api.delete_pet(pet_response.id)

def test_get_pet_by_id(new_pet):
    response = requests.get(f"{Config.BASE_PET_STORE_URL}/{new_pet.id}")
    verify_ok_response(response)

    actual_pet = Pet(**response.json())
    assert actual_pet.id == new_pet.id
    assert actual_pet.name == new_pet.name