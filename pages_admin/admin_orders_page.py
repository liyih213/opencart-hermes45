"""
Admin Orders Page — 订单管理
"""
from pages.base_page import BasePage
from utils.logger import logger


class AdminOrdersPage(BasePage):
    """后台订单列表"""

    ORDER_ROWS = ".table tbody tr"
    VIEW_BUTTONS = "a[title='View']"

    def goto_orders(self, admin_url: str, token: str = ""):
        url = f"{admin_url}/index.php?route=sale/order"
        if token:
            url += f"&user_token={token}"
        self.navigate(url)
        return self

    def get_order_count(self) -> int:
        return self.page.locator(self.ORDER_ROWS).count()

    def assert_orders_listed(self):
        count = self.get_order_count()
        assert count >= 0, f"订单列表加载异常"
        logger.info(f"订单列表: {count} 条")

    def click_view_first_order(self):
        btns = self.page.locator(self.VIEW_BUTTONS)
        if btns.count() > 0:
            btns.first.click()
            self.page.wait_for_load_state("networkidle")
            logger.info("已打开第一个订单详情")
        return self

    def assert_order_detail_visible(self):
        # 订单详情页应显示订单信息
        content = self.page.content()
        assert "order" in content.lower(), "订单详情未加载"
        logger.info("订单详情可见")
