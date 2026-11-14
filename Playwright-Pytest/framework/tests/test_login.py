import re
import pytest
from playwright.sync_api import expect

from config import SETTINGS


@pytest.mark.smoke
def test_valid_user_reaches_the_inventory(page, login_page):
    login_page.open().login(SETTINGS.user, SETTINGS.password)
    expect(page).to_have_url(re.compile(r"/inventory$"))
    expect(page.get_by_test_id("product")).to_have_count(6)


@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("", "anything", "Username is required"),
        (SETTINGS.user, "", "Password is required"),
        (SETTINGS.user, "wrong-password", "Invalid username or password"),
        ("unknown.user", "anything", "Invalid username or password"),
        ("locked.user", "anything", "This account is locked"),
    ],
    ids=["no-username", "no-password", "wrong-password", "unknown-user", "locked-user"],
)
def test_invalid_login_shows_a_clear_error(login_page, username, password, expected_error):
    login_page.open().login(username, password)
    login_page.expect_error(expected_error)


@pytest.mark.regression
def test_protected_page_redirects_anonymous_users_to_login(page):
    page.goto("/inventory")
    expect(page).to_have_url(re.compile(r"/login$"))

