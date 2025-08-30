from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def wait_until_text(driver: WebDriver, locator: (str, str), expected_text: str) -> None:
    actual_text = None
    try:
        actual_text = driver.find_element(*locator).text
    except:
        pass
    WebDriverWait(driver, 5).until(
        ec.text_to_be_present_in_element(locator, expected_text),
        message=f"\nExpected text: '{expected_text}' in element {locator}. Actual text: {actual_text}"
    )