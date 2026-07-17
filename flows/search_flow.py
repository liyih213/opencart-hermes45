"""
搜索业务流程 — 组合 HomePage + SearchResultsPage
"""
import allure
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.logger import logger


class SearchFlow:
    """搜索流程编排"""

    def __init__(self, page):
        self.home_page = HomePage(page)
        self.search_results_page = SearchResultsPage(page)

    @allure.step("搜索商品")
    def search(self, base_url: str, keyword: str):
        """从首页搜索商品"""
        self.home_page.goto_home(base_url)
        self.home_page.assert_search_bar_visible()
        self.home_page.search(keyword)
        self.search_results_page.assert_results_displayed()
        logger.info(f"✓ 搜索 '{keyword}' — 找到 {self.search_results_page.get_results_count()} 条结果")

    @allure.step("搜索无结果关键字")
    def search_no_results(self, base_url: str, keyword: str, expected_text: str):
        """搜索无效关键字"""
        self.home_page.goto_home(base_url)
        self.home_page.search(keyword)
        self.search_results_page.assert_no_results(expected_text)
        logger.info(f"✓ 搜索 '{keyword}' — 无结果")

    @allure.step("搜索并选择商品")
    def search_and_select_product(self, base_url: str, keyword: str, product_index: int = 0):
        """搜索后点击第一个结果"""
        self.search(base_url, keyword)
        self.search_results_page.click_product_by_index(product_index)
        logger.info(f"✓ 已进入商品详情页")
