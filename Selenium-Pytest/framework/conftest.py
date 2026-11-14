"""Fixtures: the application under test, the browser and the evidence collected on failure.

Run it:
    pip install -r requirements.txt
    pytest                                  # Chrome, headless, bundled demo app
    BROWSER=firefox pytest                  # or: pytest --selenium-browser firefox
    HEADLESS=0 pytest -m smoke              # watch the browser
    BASE_URL=https://staging.example.com pytest   # any other deployment
"""
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests
from selenium import webdriver

from config import DEMO_APP, SETTINGS
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

REPORTS = Path(__file__).parent / "reports"


def pytest_addoption(parser):
    parser.addoption("--selenium-browser", default=SETTINGS.browser, choices=["chrome", "firefox", "edge"])


# ---------------------------------------------------------------- application under test
def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def base_url():
    """Use BASE_URL when given, otherwise start the bundled demo app for the whole session."""
    if SETTINGS.base_url:
        yield SETTINGS.base_url
        return
    port = _free_port()
    process = subprocess.Popen(
        [sys.executable, str(DEMO_APP), "--port", str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(50):
            try:
                if requests.get(f"{url}/health", timeout=1).status_code == 200:
                    break
            except requests.RequestException:
                time.sleep(0.2)
        else:
            raise RuntimeError("demo app did not start")
        yield url
    finally:
        process.terminate()


# ---------------------------------------------------------------------------- browser
def _build_driver(browser: str) -> webdriver.Remote:
    """Selenium Manager downloads the matching driver, so no driver paths live in the code."""
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if SETTINGS.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1366,900")
        options.add_argument("--no-sandbox")  # required in most CI containers
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)
    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if SETTINGS.headless:
            options.add_argument("-headless")
        options.add_argument("--width=1366")
        options.add_argument("--height=900")
        return webdriver.Firefox(options=options)
    options = webdriver.EdgeOptions()
    if SETTINGS.headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    return webdriver.Edge(options=options)


@pytest.fixture
def driver(request):
    """A fresh browser per test: no state leaks between tests, so they can run in any order."""
    browser = _build_driver(request.config.getoption("--selenium-browser"))
    request.node.driver = browser
    yield browser
    browser.quit()


# ------------------------------------------------------------------- page objects
@pytest.fixture
def login_page(driver, base_url):
    return LoginPage(driver, base_url, SETTINGS.timeout)


@pytest.fixture
def inventory_page(driver, base_url):
    return InventoryPage(driver, base_url, SETTINGS.timeout)


@pytest.fixture
def cart_page(driver, base_url):
    return CartPage(driver, base_url, SETTINGS.timeout)


@pytest.fixture
def checkout_page(driver, base_url):
    return CheckoutPage(driver, base_url, SETTINGS.timeout)


@pytest.fixture
def logged_in(login_page, inventory_page):
    """Sign in through the UI once per test and hand back the inventory page."""
    login_page.open().login(SETTINGS.user, SETTINGS.password)
    inventory_page.wait_for_url("/inventory")
    return inventory_page


# ------------------------------------------------------------- evidence on failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    driver = getattr(item, "driver", None)
    if report.when != "call" or report.passed or driver is None:
        return
    REPORTS.mkdir(exist_ok=True)
    stem = REPORTS / item.name.replace("/", "_").replace("[", "_").replace("]", "")
    screenshot = stem.with_suffix(".png")
    driver.save_screenshot(str(screenshot))
    stem.with_suffix(".html").write_text(driver.page_source, encoding="utf-8")
    extras = getattr(report, "extras", [])
    try:
        from pytest_html import extras as html_extras

        extras.append(html_extras.image(str(screenshot)))
        extras.append(html_extras.url(driver.current_url, name="URL at failure"))
        report.extras = extras
    except ImportError:
        pass
