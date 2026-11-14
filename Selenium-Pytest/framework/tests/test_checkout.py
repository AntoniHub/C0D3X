import pytest


@pytest.mark.smoke
def test_complete_purchase_end_to_end(logged_in, cart_page, checkout_page):
    logged_in.add(2)
    logged_in.add(5)
    logged_in.open_cart()
    assert cart_page.total() == pytest.approx(17.98)
    cart_page.checkout()
    checkout_page.fill("Ada", "Lovelace", "46001").finish()
    assert checkout_page.confirmation() == "Thank you for your order"
    # The cart is emptied after the purchase.
    cart_page.open()
    assert cart_page.is_empty()


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
def test_checkout_validates_required_fields(logged_in, cart_page, checkout_page, first, last, postal, expected_error):
    logged_in.add(1)
    logged_in.open_cart()
    cart_page.checkout()
    checkout_page.fill(first, last, postal).finish()
    assert checkout_page.error_message() == expected_error

