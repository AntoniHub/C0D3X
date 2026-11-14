"""Behaviour shared by every page object.

Rules that keep the suite stable:
* Every interaction goes through an explicit wait. There are no ``time.sleep`` calls.
* Locators are ``data-testid`` selectors, so a layout or CSS change does not break tests.
* Tests never touch ``driver``; they only call methods that describe user intent.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def testid(value: str) -> tuple[str, str]:
    return By.CSS_SELECTOR, f'[data-testid="{value}"]'


class BasePage:
    path = "/"

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, timeout)

    # navigation
    def open(self):
        self.driver.get(f"{self.base_url}{self.path}")
        return self

    # waits and actions
    def visible(self, locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text: str) -> None:
        element = self.visible(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator) -> str:
        return self.visible(locator).text.strip()

    def texts_of(self, locator) -> list[str]:
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return [e.text.strip() for e in self.driver.find_elements(*locator)]

    def is_present(self, locator) -> bool:
        return bool(self.driver.find_elements(*locator))

    def select(self, locator, value: str) -> None:
        Select(self.visible(locator)).select_by_value(value)

    def wait_for_url(self, fragment: str) -> None:
        self.wait.until(EC.url_contains(fragment))

