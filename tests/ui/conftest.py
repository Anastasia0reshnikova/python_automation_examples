import logging

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from core.config import Config

logger = logging.Logger(__name__)

@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    caps = options.to_capabilities()
    caps["pageLoadStrategy"] = "eager"

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(time_to_wait=10)
    driver.maximize_window()
    logger.info(f"Opening {Config.BASE_QA_DEMO_URL} page")
    driver.get(Config.BASE_QA_DEMO_URL)
    # add cookies, loca storage elems, headers
    yield driver

    driver.quit()