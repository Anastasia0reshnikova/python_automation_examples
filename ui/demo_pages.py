from selenium.webdriver.common.by import By


class LoginPage:

    def __init__(self, d, base):
        self.d, self.base = d, base

    def open(self):
        self.d.get(f"{self.base}/login")

    def sign_in(self, user, pwd):
        self.d.find_element(By.ID,"userName").send_keys(user)
        self.d.find_element(By.ID,"password").send_keys(pwd)
        self.d.find_element(By.ID,"login").click()

