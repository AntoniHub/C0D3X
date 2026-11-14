from playwright.sync_api import Page, expect


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self.first = page.get_by_test_id("first-name")
        self.last = page.get_by_test_id("last-name")
        self.postal = page.get_by_test_id("postal-code")
        self.finish_button = page.get_by_test_id("finish")
        self.error = page.get_by_test_id("checkout-error")
        self.complete = page.get_by_test_id("order-complete")

    def fill(self, first: str = "", last: str = "", postal: str = "") -> "CheckoutPage":
        self.first.fill(first)
        self.last.fill(last)
        self.postal.fill(postal)
        return self

    def finish(self) -> None:
        self.finish_button.click()

    def expect_error(self, message: str) -> None:
        expect(self.error).to_have_text(message)

    def expect_confirmation(self) -> None:
        expect(self.complete).to_have_text("Thank you for your order")

