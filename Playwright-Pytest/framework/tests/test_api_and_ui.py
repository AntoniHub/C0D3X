"""API checks and UI/API consistency: one framework for both layers."""
import pytest
from playwright.sync_api import expect


@pytest.mark.api
@pytest.mark.regression
def test_products_endpoint_contract(api):
    response = api.get("/api/products")
    assert response.ok
    assert response.headers["content-type"].startswith("application/json")
    products = response.json()
    assert len(products) == 6
    assert len({p["id"] for p in products}) == len(products), "ids must be unique"
    for product in products:
        assert set(product) == {"id", "name", "price"}
        assert isinstance(product["price"], (int, float)) and product["price"] > 0


@pytest.mark.api
@pytest.mark.regression
def test_ui_lists_exactly_what_the_api_returns(api, inventory):
    expected = sorted(p["name"] for p in api.get("/api/products").json())
    assert inventory.product_names() == expected


@pytest.mark.api
@pytest.mark.regression
def test_unknown_route_returns_404(api):
    assert api.get("/api/does-not-exist").status == 404


@pytest.mark.regression
def test_network_failure_on_add_to_cart_is_visible_to_the_user(auth_page, inventory):
    """Simulate the backend failing: intercept the request and answer with a 500."""
    auth_page.route("**/cart/add/*", lambda route: route.fulfill(status=500, body="Service unavailable"))
    auth_page.get_by_test_id("add-1").click()
    expect(auth_page.locator("body")).to_have_text("Service unavailable")

