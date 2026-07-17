"""
测试用例: 结账模块（登录用户）
"""
import allure
import pytest
from flows.checkout_flow import CheckoutFlow
from utils.logger import logger


@allure.feature("结账模块")
class TestCheckout:

    @allure.story("登录用户完整结账")
    @allure.title("加购 → Flat Rate → COD → 下单成功")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_checkout_logged_in(self, logged_in_page, base_url):
        """登录用户：加购 MacBook → 购物车 → 配送 → 支付 → 下单"""
        flow = CheckoutFlow(logged_in_page)
        flow.checkout_as_logged_in_user(base_url, need_add_product=True, keyword="Mac")
