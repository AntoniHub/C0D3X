import re
from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.item_names = page.get_by_test_id("cart-item-name")
        self.total = page.get_by_test_id("cart-total")
        self.empty = page.get_by_test_id("cart-empty")
        self.checkout_link = page.get_by_test_id("checkout-link")

    def open(self) -> "CartPage":
        self.page.goto("/cart")
        return self

    def remove(self, product_id: int) -> None:
        self.page.get_by_test_id(f"cart-remove-{product_id}").click()

    def expect_total(self, amount: str) -> None:
        expect(self.total).to_have_text(amount)

    def checkout(self) -> None:
        self.checkout_link.click()
        expect(self.page).to_have_url(re.compile(r"/checkout$"))
