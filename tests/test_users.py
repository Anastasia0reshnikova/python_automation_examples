import os

from core.api.data_models import User


class TestUsers:
    BASIC_USER = User(username=os.getenv("BASIC_USER_NAME"), password=os.getenv("BASIC_USER_PASSWORD"))
