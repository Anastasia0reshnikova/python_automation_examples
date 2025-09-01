from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object для страницы логина"""

    # локаторы
    USERNAME_INPUT = (By.ID, "userName")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login")

    def __init__(self, driver, base_url, timeout: int = 5):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        """Открыть страницу логина"""
        self.driver.get(f"{self.base_url}/login")
        # убедиться, что форма загрузилась
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        return self

    def sign_in(self, username: str, password: str):
        """Авторизоваться пользователем"""
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BTN).click()
        # ждём, пока исчезнет кнопка логина (или появится другой элемент)
        self.wait.until(EC.invisibility_of_element_located(self.LOGIN_BTN))
        # возвращаем новую страницу, например HomePage
        # return HomePage(self.driver, self.base_url)
        return self
