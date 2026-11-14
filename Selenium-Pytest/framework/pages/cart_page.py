from .base_page import BasePage, testid


class CartPage(BasePage):
    path = "/cart"
    ITEM_NAMES = testid("cart-item-name")
    TOTAL = testid("cart-total")
    EMPTY = testid("cart-empty")
    CHECKOUT = testid("checkout-link")

    def item_names(self) -> list[str]:
        return self.texts_of(self.ITEM_NAMES)

    def total(self) -> float:
        return float(self.text_of(self.TOTAL))

    def remove(self, product_id: int):
        self.click(testid(f"cart-remove-{product_id}"))
        return self

    def is_empty(self) -> bool:
        return self.visible(self.EMPTY).is_displayed()

    def checkout(self):
        self.click(self.CHECKOUT)
        self.wait_for_url("/checkout")
