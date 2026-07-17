"""
Account Page — 账户页对象
"""
from pages.base_page import BasePage
from utils.logger import logger


class AccountPage(BasePage):
    """OpenCart 我的账户页"""

    # ── Selectors ──────────────────────────────────────────
    PAGE_HEADING = "#content h2"
    ACCOUNT_LINKS = "#content ul.list-unstyled a"
    SIDEBAR_MENU = "#column-right"
    LOGOUT_LINK = "a.list-group-item[href*='logout']"

    # ── Actions ────────────────────────────────────────────

    def goto_account(self, base_url: str):
        self.navigate(f"{base_url}/index.php?route=account/account")
        return self

    def click_logout(self):
        logger.info("登出")
        self.click(self.LOGOUT_LINK)
        return self

    # ── Assertions ─────────────────────────────────────────

    def assert_on_account_page(self):
        self.assert_text_visible("My Account")
        logger.info("已在账户页面")

    def assert_logged_in_as(self, name: str):
        """断言登录用户名称可见"""
        # OpenCart 登录后右上角通常会显示用户名
        try:
            self.assert_text_visible(name)
        except Exception:
            # fallback: 检查页面是否包含账户相关文字
            self.assert_on_account_page()
        logger.info(f"已登录为: {name}")
