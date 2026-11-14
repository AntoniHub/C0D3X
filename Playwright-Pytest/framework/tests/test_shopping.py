import re
import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_added_product_appears_in_the_cart(inventory, cart):
    inventory.add(1)
    expect(inventory.cart_count).to_have_text("1")
    inventory.open_cart()
    expect(cart.item_names).to_have_text(["Backpack"])
    cart.expect_total("29.99")


@pytest.mark.regression
def test_cart_total_is_the_sum_of_its_items(inventory, cart):
    for product_id in (1, 2, 5):  # 29.99 + 9.99 + 7.99
        inventory.add(product_id)
    inventory.open_cart()
    cart.expect_total("47.97")


@pytest.mark.regression
def test_removing_the_last_item_empties_the_cart(inventory, cart):
    inventory.add(4)
    inventory.open_cart()
    cart.remove(4)
    expect(cart.empty).to_be_visible()
    cart.expect_total("0.00")


@pytest.mark.regression
def test_products_can_be_sorted_by_price(inventory):
    inventory.sort_by("price")
    prices = inventory.product_prices()
    assert prices == sorted(prices)


@pytest.mark.regression
def test_logout_ends_the_session(inventory, auth_page):
    inventory.logout()
    auth_page.goto("/inventory")
    expect(auth_page).to_have_url(re.compile(r"/login$"))


@pytest.mark.smoke
def test_complete_purchase_end_to_end(inventory, cart, checkout):
    inventory.add(2)
    inventory.add(5)
    inventory.open_cart()
    cart.expect_total("17.98")
    cart.checkout()
    checkout.fill("Ada", "Lovelace", "46001").finish()
    checkout.expect_confirmation()
    expect(cart.open().empty).to_be_visible()


@pytest.mark.regression
@pytest.mark.parametrize(
    "first, last, postal, expected_error",
    [
        ("", "Lovelace", "46001", "First name is required"),
        ("Ada", "", "46001", "Last name is required"),
        ("Ada", "Lovelace", "", "Postal code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postal-code"],
)
def test_checkout_validates_required_fields(inventory, cart, checkout, first, last, postal, expected_error):
    inventory.add(1)
    inventory.open_cart()
    cart.checkout()
    checkout.fill(first, last, postal).finish()
    checkout.expect_error(expected_error)
