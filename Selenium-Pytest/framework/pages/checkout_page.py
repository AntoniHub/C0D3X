from .base_page import BasePage, testid


class CheckoutPage(BasePage):
    path = "/checkout"
    FIRST = testid("first-name")
    LAST = testid("last-name")
    POSTAL = testid("postal-code")
    FINISH = testid("finish")
    ERROR = testid("checkout-error")
    COMPLETE = testid("order-complete")

    def fill(self, first: str = "", last: str = "", postal: str = ""):
        self.type(self.FIRST, first)
        self.type(self.LAST, last)
        self.type(self.POSTAL, postal)
        return self

    def finish(self):
        self.click(self.FINISH)
        return self

    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    def confirmation(self) -> str:
        return self.text_of(self.COMPLETE)
