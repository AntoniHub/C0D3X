from .base_page import BasePage, testid


class LoginPage(BasePage):
    path = "/login"
    USERNAME = testid("username")
    PASSWORD = testid("password")
    SUBMIT = testid("login-button")
    ERROR = testid("login-error")

    def login(self, username: str, password: str):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return self

    def error_message(self) -> str:
        return self.text_of(self.ERROR)

