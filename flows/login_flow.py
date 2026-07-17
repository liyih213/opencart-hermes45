"""
登录业务流程 — 组合 LoginPage + AccountPage
"""
import allure
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from utils.logger import logger


class LoginFlow:
    """登录流程编排"""

    def __init__(self, page):
        self.login_page = LoginPage(page)
        self.account_page = AccountPage(page)

    @allure.step("用户登录")
    def login(self, base_url: str, email: str, password: str):
        """完整登录流程"""
        self.login_page.goto_login(base_url)
        self.login_page.login(email, password)
        self.login_page.assert_login_success()
        logger.info(f"✓ 登录成功 — {email}")

    @allure.step("用户登录 — 预期失败")
    def login_expect_fail(self, base_url: str, email: str, password: str, expected_error: str):
        """登录并验证错误提示"""
        self.login_page.goto_login(base_url)
        self.login_page.login(email, password)
        self.login_page.assert_login_error(expected_error)
        logger.info(f"✓ 登录失败符合预期 — {email}")

    @allure.step("用户登出")
    def logout(self, base_url: str):
        """登出流程 — 要求 page 已处于登录态"""
        self.account_page.click_logout()
        # OpenCart 4.x 点击 logout 后停留在 /account/logout，显示确认信息
        self.login_page.page.wait_for_load_state("networkidle")
        # 验证已登出：URL 包含 logout 或回到 login 页
        current = self.login_page.page.url
        assert "logout" in current or "login" in current, \
            f"登出后未跳转到预期页面: {current}"
        logger.info("✓ 登出成功")
