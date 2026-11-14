import pytest


@pytest.mark.smoke
def test_added_product_appears_in_the_cart(logged_in, cart_page):
    logged_in.add(1)
    assert logged_in.cart_count() == 1
    logged_in.open_cart()
    assert cart_page.item_names() == ["Backpack"]
    assert cart_page.total() == 29.99


@pytest.mark.regression
def test_cart_total_is_the_sum_of_its_items(logged_in, cart_page):
    for product_id in (1, 2, 5):  # 29.99 + 9.99 + 7.99
        logged_in.add(product_id)
    logged_in.open_cart()
    assert cart_page.total() == pytest.approx(47.97)


@pytest.mark.regression
def test_removing_the_last_item_empties_the_cart(logged_in, cart_page):
    logged_in.add(4)
    logged_in.open_cart()
    cart_page.remove(4)
    assert cart_page.is_empty()
    assert cart_page.total() == 0


@pytest.mark.regression
def test_products_can_be_sorted_by_price(logged_in):
    logged_in.sort_by("price")
    prices = logged_in.product_prices()
    assert prices == sorted(prices)


@pytest.mark.regression
def test_products_are_sorted_by_name_by_default(logged_in):
    names = logged_in.product_names()
    assert names == sorted(names)
