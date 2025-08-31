import logging

import pytest

from api_pet_service.api_client import FastApiClient
from helpers.api_assertions import verify_ok_response
from tests.test_users import TestUsers

logger = logging.getLogger(__name__)


@pytest.fixture
def client():
    return FastApiClient(user=TestUsers.FASTAPI_USER)


@pytest.fixture(autouse=True)
def set_up():
    logger.info("Start test")
    yield
    logger.info("Finish test")


def test_get_pets(client):
    response = client.get_pets()
    verify_ok_response(response)
    logger.info(response.json())