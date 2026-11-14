from selenium.webdriver.common.by import By

from .base_page import BasePage, testid


class InventoryPage(BasePage):
    path = "/inventory"
    NAMES = testid("product-name")
    PRICES = testid("product-price")
    SORT = testid("sort")
    CART_COUNT = testid("cart-count")
    CART_LINK = testid("cart-link")
    LOGOUT = testid("logout")

    def product_names(self) -> list[str]:
        return self.texts_of(self.NAMES)

    def product_prices(self) -> list[float]:
        return [float(p) for p in self.texts_of(self.PRICES)]

    def sort_by(self, value: str):
        self.select(self.SORT, value)
        # The page reloads: wait until the selected option is the requested one.
        self.wait.until(lambda d: d.find_element(By.CSS_SELECTOR, '[data-testid="sort"]').get_attribute("value") == value)
        return self

    def add(self, product_id: int):
        self.click(testid(f"add-{product_id}"))
        self.visible(testid(f"remove-{product_id}"))  # the button flips once the cart is updated
        return self

    def remove(self, product_id: int):
        self.click(testid(f"remove-{product_id}"))
        self.visible(testid(f"add-{product_id}"))
        return self

    def cart_count(self) -> int:
        return int(self.text_of(self.CART_COUNT))

    def open_cart(self):
        self.click(self.CART_LINK)
        self.wait_for_url("/cart")

    def logout(self):
        self.click(self.LOGOUT)
        self.wait_for_url("/login")
