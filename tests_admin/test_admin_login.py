"""
后台测试: 登录
"""
import allure
import pytest
from pages_admin.admin_login_page import AdminLoginPage


@allure.feature("Admin - 登录")
class TestAdminLogin:

    @allure.title("后台登录成功 → 跳转 Dashboard")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_admin_login_success(self, page, admin_base_url, admin_test_data):
        lp = AdminLoginPage(page)
        lp.goto_login(admin_base_url)
        account = admin_test_data["admin"]
        lp.login(account["username"], account["password"])
        lp.assert_login_success()
