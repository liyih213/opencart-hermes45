"""
测试用例: 购物车模块
"""
import allure
import pytest
from flows.cart_flow import CartFlow
from utils.logger import logger


@allure.feature("购物车模块")
class TestCart:

    @allure.story("添加商品到购物车")
    @allure.title("搜索 Mac 并添加到购物车")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize("keyword", ["Mac", "iPhone"])
    def test_add_product_to_cart(self, page, base_url, keyword):
        """搜索商品 → 添加至购物车 → 验证购物车非空"""
        flow = CartFlow(page)
        flow.add_product_to_cart(base_url, keyword)
        flow.view_cart(base_url)

    @allure.story("修改购物车数量")
    @allure.title("将购物车商品数量改为 3")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_cart_quantity(self, page, base_url):
        """添加商品后修改数量为 3"""
        flow = CartFlow(page)
        flow.add_product_to_cart(base_url, "Mac", quantity=1)
        flow.update_cart_quantity(base_url, index=0, new_quantity=3)

    @allure.story("移除购物车商品")
    @allure.title("添加多个商品后逐一清除")
    @allure.severity(allure.severity_level.NORMAL)
    def test_remove_from_cart(self, page, base_url):
        """添加商品 → 清空购物车 → 验证为空"""
        flow = CartFlow(page)
        flow.add_product_to_cart(base_url, "Mac")
        flow.clear_cart(base_url)
        flow.verify_empty_cart(base_url)

    @allure.story("空购物车显示")
    @allure.title("未添加商品时购物车为空")
    @allure.severity(allure.severity_level.MINOR)
    def test_empty_cart_by_default(self, page, base_url):
        """不添加商品，直接进入购物车 → 应显示空"""
        flow = CartFlow(page)
        flow.verify_empty_cart(base_url)
