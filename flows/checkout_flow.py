"""
结账业务流程 — 组合 CartPage + CheckoutPage（登录用户结账）
"""
import allure
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.logger import logger


class CheckoutFlow:
    """结账流程编排"""

    def __init__(self, page):
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)

    @allure.step("登录用户完整结账流程")
    def checkout_as_logged_in_user(self, base_url: str, need_add_product: bool = True, keyword: str = "Mac"):
        """加购 → 购物车 → 完整结账流程"""
        if need_add_product:
            from flows.cart_flow import CartFlow
            cart_flow = CartFlow(self.cart_page.page)
            cart_flow.add_product_to_cart(base_url, keyword)

        # 进入购物车
        self.cart_page.goto_cart(base_url)
        self.cart_page.assert_cart_not_empty()

        # 去结账
        self.cart_page.click_checkout()
        self.checkout_page.assert_on_checkout_page()

        # 执行结账
        self.checkout_page.checkout_logged_in()

        # 验证下单成功
        self.checkout_page.assert_order_success()
        logger.info("✓ 结账 — 下单成功")
