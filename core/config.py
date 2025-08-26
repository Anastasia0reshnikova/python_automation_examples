import os


class Config:
    BASE_DEMO_URL = os.getenv("BASE_DEMO_URL")
    BASE_STORE_URL = os.getenv("BASE_STORE_URL")