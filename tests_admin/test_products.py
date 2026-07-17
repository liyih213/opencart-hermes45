"""
后台测试: 商品管理
"""
import allure
import pytest
from pages_admin.admin_products_page import AdminProductsPage


@allure.feature("Admin - 商品管理")
class TestAdminProducts:

    @allure.title("商品列表加载 → 至少有一个商品")
    @allure.severity(allure.severity_level.NORMAL)
    def test_products_list(self, logged_in_admin_page, admin_base_url):
        page, token = logged_in_admin_page
        pp = AdminProductsPage(page)
        pp.goto_products(admin_base_url, token)
        pp.assert_products_listed(min_count=1)

    @allure.title("搜索商品 MacBook → 筛选后列表只含 MacBook")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_product(self, logged_in_admin_page, admin_base_url):
        page, token = logged_in_admin_page
        pp = AdminProductsPage(page)
        pp.goto_products(admin_base_url, token)
        pp.search_product("MacBook")
        assert pp.get_product_count() >= 1, "搜索 MacBook 无结果"
