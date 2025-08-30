from time import sleep
from uuid import uuid4

import pytest

from core.api.data_models import Pet, Category
from core.api.petstore_api_client import PetAPI
from tests.test_users import TestUsers

new_pet_data = Pet(
    category=Category(id=1, name="home"),
    name=f"kitty_{uuid4().hex[:8]}",
    photoUrls=["photo_url"],
    status="available")

@pytest.fixture(scope='module')
def pet_api():
    return PetAPI(user=TestUsers.BASIC_USER)

@pytest.fixture
def new_pet(pet_api):
     response = pet_api.add_new_pet(new_pet=new_pet_data)
     response.raise_for_status()
     pet_response = Pet(**response.json()) #** - deserialization
     sleep(5)
     yield pet_response #for shearing to every test

     pet_api.delete_pet(pet_response.id)


def test_add_new_pet(pet_api, new_pet):
    assert new_pet.id is not None
    assert new_pet.name == new_pet_data.name
    assert new_pet.category.id is not None
    assert new_pet.category.name == new_pet_data.category.name
    assert new_pet.photoUrls == new_pet_data.photoUrls
    assert new_pet.status == new_pet_data.status

def test_update_existing_pet():
    pass

def test_get_pet_by_id(pet_api, new_pet):
    response = pet_api.get_pet_by_id(pet_id=new_pet.id)
    assert response.status_code == 200
    get_pet_response = Pet(**response.json())
    assert get_pet_response.name == new_pet.name
    assert get_pet_response.category.id is not None
    assert get_pet_response.category.name == new_pet.category.name

@pytest.mark.parametrize("status", ["available", "pending", "sold"])
def test_find_pet_by_status(status):
    pass

def test_update_pet_by_id():
    pass

def test_delete_pet_by_id(pet_api, new_pet):
    response_delete = pet_api.delete_pet(pet_id=new_pet.id)
    assert response_delete.status_code == 200
    response_get = pet_api.get_pet_by_id(pet_id=new_pet.id)
    assert response_get.status_code == 404

@pytest.mark.parametrize(
    "pet_id",
    ["tratata", "_", "12345_"]
)
def test_delete_pet_by_wrong_id(pet_api, pet_id):
    response_delete = pet_api.delete_pet(pet_id=pet_id)
    assert response_delete.status_code == 404
    assert response_delete.reason == "Not Found"