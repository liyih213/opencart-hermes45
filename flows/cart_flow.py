"""
购物车业务流程 — 组合 HomePage + SearchResultsPage + ProductPage + CartPage
"""
import allure
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.logger import logger


class CartFlow:
    """购物车流程编排"""

    def __init__(self, page):
        self.home_page = HomePage(page)
        self.search_results_page = SearchResultsPage(page)
        self.product_page = ProductPage(page)
        self.cart_page = CartPage(page)

    @allure.step("添加商品到购物车")
    def add_product_to_cart(self, base_url: str, keyword: str, quantity: int = 1):
        """搜索商品 → 进入详情 → 添加到购物车"""
        # 搜索
        self.home_page.goto_home(base_url)
        self.home_page.search(keyword)
        self.search_results_page.assert_results_displayed()

        # 进入商品详情
        self.search_results_page.click_product_by_index(0)

        # 添加至购物车
        self.product_page.add_to_cart(quantity)
        self.product_page.assert_add_to_cart_success()
        # 等待 AJAX 写入 session
        self.product_page.page.wait_for_timeout(1000)
        logger.info(f"✓ '{keyword}' ×{quantity} 已加入购物车")

    @allure.step("查看并验证购物车")
    def view_cart(self, base_url: str):
        self.cart_page.goto_cart(base_url)
        self.cart_page.assert_cart_not_empty()
        return self.cart_page

    @allure.step("修改购物车数量")
    def update_cart_quantity(self, base_url: str, index: int, new_quantity: int):
        """修改购物车中商品数量"""
        self.cart_page.goto_cart(base_url)
        self.cart_page.update_quantity(index, new_quantity)
        self.cart_page.click_update()
        self.cart_page.assert_quantity_is(index, new_quantity)
        logger.info(f"✓ 数量已更新为 {new_quantity}")

    @allure.step("清空购物车")
    def clear_cart(self, base_url: str):
        """逐一移除购物车中所有商品"""
        self.cart_page.goto_cart(base_url)
        while self.cart_page.get_cart_items_count() > 0:
            self.cart_page.remove_item(0)
            self.cart_page.page.wait_for_timeout(1000)
        logger.info("✓ 购物车已清空")

    @allure.step("验证购物车为空")
    def verify_empty_cart(self, base_url: str):
        self.cart_page.goto_cart(base_url)
        self.cart_page.assert_cart_empty()
        logger.info("✓ 购物车为空")
