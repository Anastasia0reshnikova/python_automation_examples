import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
UI-тесты (pytest + selenium)
"""

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(3)
    yield drv
    drv.quit()

# 1. Login form
def test_login_success(driver):
    driver.get("https://demoqa.com/login")
    driver.find_element(By.ID, "userName").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("testpass")
    driver.find_element(By.ID, "login").click()
    WebDriverWait(driver, 5).until(EC.url_contains("profile"))

# 2. Error message
def test_login_error(driver):
    driver.get("https://demoqa.com/login")
    driver.find_element(By.ID, "login").click()
    error = driver.find_element(By.ID, "name").text
    assert "Invalid" in error or "required" in error

# 3. Search box
def test_search(driver):
    driver.get("https://demoqa.com/books")
    driver.find_element(By.ID, "searchBox").send_keys("Git")
    rows = driver.find_elements(By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")
    assert any("Git" in row.text for row in rows)

# 4. Checkbox
def test_checkbox(driver):
    driver.get("https://demoqa.com/checkbox")
    cb = driver.find_element(By.CLASS_NAME, "rct-checkbox")
    cb.click()
    assert "rct-icon-check" in cb.find_element(By.XPATH, "..").get_attribute("innerHTML")

# 5. Dropdown
def test_dropdown(driver):
    driver.get("https://demoqa.com/select-menu")
    dropdown = driver.find_element(By.ID, "oldSelectMenu")
    from selenium.webdriver.support.ui import Select
    Select(dropdown).select_by_visible_text("Green")
    assert dropdown.get_attribute("value") == "2"

# 6. Dynamic element
def test_wait_for_button(driver):
    driver.get("https://demoqa.com/dynamic-properties")
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "enableAfter"))
    )
    assert btn.is_enabled()

# 7. Navigation
def test_navigation(driver):
    driver.get("https://demoqa.com")
    driver.find_element(By.CSS_SELECTOR, "div.card:nth-child(1)").click()
    WebDriverWait(driver, 5).until(EC.url_contains("elements"))
