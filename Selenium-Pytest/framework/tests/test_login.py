import pytest

from config import SETTINGS


@pytest.mark.smoke
def test_valid_user_reaches_the_inventory(login_page, inventory_page):
    login_page.open().login(SETTINGS.user, SETTINGS.password)
    inventory_page.wait_for_url("/inventory")
    assert len(inventory_page.product_names()) == 6


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
    assert login_page.error_message() == expected_error


@pytest.mark.regression
def test_protected_page_redirects_anonymous_users_to_login(inventory_page, login_page):
    inventory_page.open()
    inventory_page.wait_for_url("/login")
    assert login_page.is_present(login_page.USERNAME)


@pytest.mark.regression
def test_logout_ends_the_session(logged_in, inventory_page):
    inventory_page.logout()
    inventory_page.open()
    inventory_page.wait_for_url("/login")
