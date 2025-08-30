import os


class Config:
    BASE_DEMO_URL = os.getenv("BASE_DEMO_URL")
    BASE_QA_DEMO_URL = os.getenv("BASE_QA_DEMO_URL")
    BASE_PET_STORE_URL = os.getenv("BASE_PET_STORE_URL")