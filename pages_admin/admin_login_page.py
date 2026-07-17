"""
Admin Login Page — 后台登录页
"""
from pages.base_page import BasePage
from utils.logger import logger


class AdminLoginPage(BasePage):
    """OpenCart 后台登录页"""

    USERNAME_INPUT = "#input-username"
    PASSWORD_INPUT = "#input-password"
    LOGIN_BUTTON = "button[type='submit']"
    DASHBOARD_HEADER = "#content .page-header"

    def goto_login(self, admin_url: str):
        self.navigate(admin_url)
        return self

    def login(self, username: str, password: str):
        logger.info(f"后台登录: {username}")
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.page.wait_for_timeout(3000)
        self.page.wait_for_load_state("networkidle")
        return self

    def assert_login_success(self):
        self.assert_url_contains("route=common/dashboard")
        logger.info("后台登录成功")
