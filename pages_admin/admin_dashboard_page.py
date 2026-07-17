"""
Admin Dashboard Page — 后台首页
"""
from pages.base_page import BasePage
from utils.logger import logger


class AdminDashboardPage(BasePage):
    """OpenCart 后台仪表盘"""

    def goto_dashboard(self, admin_url: str):
        self.navigate(f"{admin_url}/index.php?route=common/dashboard")
        return self

    def assert_on_dashboard(self):
        self.assert_url_contains("route=common/dashboard")
        logger.info("已在后台 Dashboard")
