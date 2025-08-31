import logging

import requests
from requests import Session, Response

from core.api.data_models import User
from core.config import Config

logger = logging.getLogger(__name__)


def auth(user: User):
    # data = {"username": user.username, "password": user.password}
    if user is None:
        return None
    request = requests.post(f"{Config.BASE_URL}/auth/login", user.model_dump_json())
    return request.json()["access_token"]


class FastApiClient:

    def __init__(self, user: User = None):
        self.base_url = Config.BASE_URL
        self.api = Session()
        token = auth(user)
        self.api.headers.update({"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
        logger.info(f"{self.base_url}")

    def get_pets(self):
        response = self.api.get(url=f"{self.base_url}/pets")
        log_request(response)
        return response


def log_request(response: Response):
    logger.info(f"{response.request.method} {response.request.url} - {response.status_code}")
