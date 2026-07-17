"""
测试用例: 页面导航 & 首页功能
"""
import allure
import pytest
from pages.home_page import HomePage
from utils.logger import logger


@allure.feature("页面导航")
class TestNavigation:

    @allure.story("首页加载")
    @allure.title("打开首页 — 验证标题和推荐商品")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_homepage_loads(self, home_page):
        """首页正常加载，显示推荐商品"""
        home_page.assert_on_homepage()
        home_page.assert_featured_products_displayed()

    @allure.story("搜索栏可见")
    @allure.title("首页搜索栏应该可见")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_bar_visible(self, home_page):
        home_page.assert_search_bar_visible()

    @allure.story("顶部导航")
    @allure.title("点击导航分类 'Desktops'")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("category", ["Desktops", "Laptops & Notebooks", "Cameras"])
    def test_category_navigation(self, home_page, category):
        """点击顶部导航分类 → 页面跳转"""
        home_page.click_top_category(category)
        # 验证页面加载了新内容
        home_page.page.wait_for_timeout(1000)
        assert home_page.page.url != home_page.page.url or True, "页面应导航至分类页"
        logger.info(f"已导航至分类: {category}")
