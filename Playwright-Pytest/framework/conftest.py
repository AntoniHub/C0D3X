"""Fixtures for the Playwright reference framework.

Key ideas:
* the application under test is started once per session (or BASE_URL is used);
* the user signs in ONCE through the UI and the session is reused as storage state, so
  tests that are not about login start already authenticated (faster and less flaky);
* every test gets its own isolated browser context;
* trace, video and screenshot are kept for failures only (see pytest.ini).

Run it:
    pip install -r requirements.txt && playwright install --with-deps chromium firefox
    pytest                                # Chromium
    pytest --browser firefox              # or webkit
    pytest --headed --slowmo 300 -m smoke # watch it
    playwright show-trace reports/artifacts/<test>/trace.zip
"""
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests
from playwright.sync_api import APIRequestContext, Playwright, expect

from config import DEMO_APP, SETTINGS
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

expect.set_options(timeout=SETTINGS.expect_timeout_ms)


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def base_url():
    """Overrides the pytest-playwright fixture: start the bundled demo app unless BASE_URL is set."""
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


@pytest.fixture(scope="session")
def auth_state(browser, base_url, tmp_path_factory) -> str:
    """Log in once and save cookies and storage; later contexts start already signed in."""
    path = tmp_path_factory.mktemp("auth") / "state.json"
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    LoginPage(page).open().login(SETTINGS.user, SETTINGS.password)
    expect(page).to_have_url(re.compile(r"/inventory$"))
    context.storage_state(path=str(path))
    context.close()
    return str(path)


@pytest.fixture
def auth_page(browser, base_url, auth_state, request):
    """A page in a fresh, already authenticated context. Records a trace for failed tests."""
    context = browser.new_context(base_url=base_url, storage_state=auth_state)
    context.tracing.start(screenshots=True, snapshots=True)
    page = context.new_page()
    yield page
    failed = getattr(request.node, "rep_call", None) is not None and request.node.rep_call.failed
    if failed:
        out = Path("reports/artifacts") / request.node.name.replace("[", "_").replace("]", "")
        out.mkdir(parents=True, exist_ok=True)
        context.tracing.stop(path=str(out / "auth-trace.zip"))
        page.screenshot(path=str(out / "auth-failure.png"))
    else:
        context.tracing.stop()
    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, f"rep_{call.when}", outcome.get_result())


# -------------------------------------------------------------------- page objects
@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory(auth_page):
    return InventoryPage(auth_page).open()


@pytest.fixture
def cart(auth_page):
    return CartPage(auth_page)


@pytest.fixture
def checkout(auth_page):
    return CheckoutPage(auth_page)


# ---------------------------------------------------------------------- API client
@pytest.fixture(scope="session")
def api(playwright: Playwright, base_url) -> APIRequestContext:
    """Playwright's own HTTP client: same engine, no extra dependency for API checks."""
    context = playwright.request.new_context(base_url=base_url)
    yield context
    context.dispose()
