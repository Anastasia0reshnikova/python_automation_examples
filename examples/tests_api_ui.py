# UI + API (пример условный)

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def test_register_and_login(driver):
    # через API создаём пользователя
    r = requests.post(f"{BASE_URL}/user", json={"username": "api_user", "password": "1234"})
    assert r.status_code == 200

    # логинимся через UI
    driver.get("https://demoqa.com/login")
    driver.find_element(By.ID, "userName").send_keys("api_user")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.ID, "login").click()
    WebDriverWait(driver, 5).until(EC.url_contains("profile"))

# Проверка валидации
def test_invalid_email(driver):
    driver.get("https://demoqa.com/text-box")
    driver.find_element(By.ID, "userEmail").send_keys("not_an_email")
    driver.find_element(By.ID, "submit").click()
    email = driver.find_element(By.ID, "userEmail")
    assert "field-error" in email.get_attribute("class")
