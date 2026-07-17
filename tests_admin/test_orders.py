"""
后台测试: 订单管理
"""
import allure
import pytest
from pages_admin.admin_orders_page import AdminOrdersPage


@allure.feature("Admin - 订单管理")
class TestAdminOrders:

    @allure.title("订单列表加载")
    @allure.severity(allure.severity_level.NORMAL)
    def test_orders_list(self, logged_in_admin_page, admin_base_url):
        page, token = logged_in_admin_page
        op = AdminOrdersPage(page)
        op.goto_orders(admin_base_url, token)
        op.assert_orders_listed()

    @allure.title("查看第一个订单详情（如有）")
    @allure.severity(allure.severity_level.MINOR)
    def test_view_order_detail(self, logged_in_admin_page, admin_base_url):
        page, token = logged_in_admin_page
        op = AdminOrdersPage(page)
        op.goto_orders(admin_base_url, token)
        if op.get_order_count() > 0:
            op.click_view_first_order()
            op.assert_order_detail_visible()
        else:
            pytest.skip("没有订单数据，跳过")
