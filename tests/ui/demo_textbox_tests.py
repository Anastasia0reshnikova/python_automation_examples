import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from core.config import Config
from helpers.wd_assertions import wait_until_text

"""
actions:
init chrome webdriver;
open browser
goto expected page
fill form
check it is filled
"""


@pytest.fixture(autouse=True)
def setup(driver):
    driver.get(f"{Config.BASE_QA_DEMO_URL}/text-box")


def test_fill_form_correctly(driver):
    expected_name = "User name"
    expected_email = "testuser@gmailtest.com"
    expected_address = "Bcn city"

    driver.find_element(By.ID, "userName").send_keys(expected_name)
    driver.find_element(By.ID, "userEmail").send_keys(expected_email)
    driver.find_element(By.ID, "currentAddress").send_keys(expected_address)
    driver.find_element(By.CSS_SELECTOR, "#userForm #submit").click()

    wait_until_text(driver, (By.CSS_SELECTOR, "#output #name"), expected_name)
    wait_until_text(driver, (By.CSS_SELECTOR, "#output #email"), expected_email)
    wait_until_text(driver, (By.CSS_SELECTOR, "#output #currentAddress"), "tataaaaaa")