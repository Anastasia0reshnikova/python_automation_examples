import logging

from core.config import Config
from requests import Session, Response

from core.data_models import Pet

"""
Every client should have base_url and api attributes.
Base url should be the base url of the api and api should be a requests session.
"""

logger = logging.getLogger(__name__)


class PetAPI:

    def __init__(self):
        self.base_url = f"{Config.BASE_PET_STORE_URL}/pet"
        self.api = Session()
        self.api.headers.update({"Content-Type": "application/json"})

    def add_new_pet(self, new_pet: Pet):
        response = self.api.post(url=self.base_url, data=new_pet.model_dump_json())
        log_request(response)
        return response

    def get_pet_by_id(self, pet_id: int):
        response = self.api.get(url=f"{self.base_url}/{pet_id}")
        log_request(response)
        return response

    def update_pet(self, pet: Pet):
        response = self.api.put(url=f"{self.base_url}/{pet.id}", data=pet.model_dump_json())
        log_request(response)
        return response

    def delete_pet(self, pet_id: int):
        response = self.api.delete(url=f"{self.base_url}/{pet_id}")
        log_request(response)
        return response

    def find_pets_by_status(self, status: list[str]):
        response = self.api.get(url=f"{self.base_url}/findByStatus?status={status[0]}")
        log_request(response)
        return response


class UserAPI:

    def __init__(self):
        self.base_url = f"{Config.BASE_PET_STORE_URL}/user"
        self.api = Session()
        self.api.headers.update({"Content-Type": "application/json"})



class StoreAPI:

    def __init__(self):
        self.base_url = f"{Config.BASE_PET_STORE_URL}/store"
        self.api = Session()
        self.api.headers.update({"Content-Type": "application/json"})


def log_request(response: Response):
    logger.info(f"{response.request.method} {response.request.url} - {response.status_code}")