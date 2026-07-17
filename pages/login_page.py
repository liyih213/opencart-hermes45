"""
Login Page — 登录页面对象
"""
from pages.base_page import BasePage
from utils.logger import logger


class LoginPage(BasePage):
    """OpenCart 登录页"""

    # ── Selectors ──────────────────────────────────────────
    EMAIL_INPUT = "#input-email"
    PASSWORD_INPUT = "#input-password"
    LOGIN_BUTTON = "#content button[type='submit']"
    LOGOUT_LINK = "a.list-group-item[href*='logout']"
    ERROR_ALERT = ".alert-danger"
    MY_ACCOUNT_LINK = "text=My Account"

    # ── Actions ────────────────────────────────────────────

    def goto_login(self, base_url: str):
        """打开登录页面"""
        self.navigate(f"{base_url}/index.php?route=account/login")
        return self

    def enter_email(self, email: str):
        self.fill(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str):
        self.fill(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        self.page.wait_for_load_state("networkidle")
        return self

    def login(self, email: str, password: str):
        """完整登录流程"""
        logger.info(f"正在登录: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self

    def click_logout(self):
        self.click(self.LOGOUT_LINK)
        return self

    # ── Assertions ─────────────────────────────────────────

    def assert_login_success(self):
        """断言登录成功（通过 URL 跳转到 account 页面判断）"""
        self.assert_url_contains("account/account")
        logger.info("登录成功")

    def assert_login_error(self, expected_text: str | None = None):
        """断言出现登录错误提示"""
        self.assert_element_visible(self.ERROR_ALERT)
        if expected_text:
            self.assert_text_contains(self.ERROR_ALERT, expected_text)
        logger.info(f"登录失败 — 错误提示符合预期")

    def assert_on_login_page(self):
        self.assert_url_contains("account/login")
