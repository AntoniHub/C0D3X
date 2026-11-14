import re
from playwright.sync_api import Page, expect


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.names = page.get_by_test_id("product-name")
        self.prices = page.get_by_test_id("product-price")
        self.sort = page.get_by_test_id("sort")
        self.cart_count = page.get_by_test_id("cart-count")
        self.cart_link = page.get_by_test_id("cart-link")
        self.logout_link = page.get_by_test_id("logout")

    def open(self) -> "InventoryPage":
        self.page.goto("/inventory")
        return self

    def product_names(self) -> list[str]:
        return self.names.all_inner_texts()

    def product_prices(self) -> list[float]:
        return [float(p) for p in self.prices.all_inner_texts()]

    def sort_by(self, value: str) -> None:
        self.sort.select_option(value)
        expect(self.sort).to_have_value(value)

    def add(self, product_id: int) -> None:
        self.page.get_by_test_id(f"add-{product_id}").click()
        expect(self.page.get_by_test_id(f"remove-{product_id}")).to_be_visible()

    def open_cart(self) -> None:
        self.cart_link.click()
        expect(self.page).to_have_url(re.compile(r"/cart$"))

    def logout(self) -> None:
        self.logout_link.click()
        expect(self.page).to_have_url(re.compile(r"/login$"))
