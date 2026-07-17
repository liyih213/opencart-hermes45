"""
测试用例: 登录模块
"""
import allure
import pytest
from flows.login_flow import LoginFlow
from utils.logger import logger


@allure.feature("登录模块")
class TestLogin:

    @allure.story("有效账号登录")
    @allure.title("使用正确账号密码登录")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_valid_login(self, page, base_url, test_data):
        """正例：demo / demo 登录成功"""
        account = test_data["accounts"]["valid"]
        flow = LoginFlow(page)
        flow.login(base_url, account["email"], account["password"])

    @allure.story("无效账号登录")
    @allure.title("使用错误密码登录应提示错误")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_invalid_login(self, page, base_url, test_data):
        """反例：错误账号密码 → 显示错误提示"""
        account = test_data["accounts"]["invalid"]
        flow = LoginFlow(page)
        flow.login_expect_fail(
            base_url,
            account["email"],
            account["password"],
            account["expected_error"],
        )

    @allure.story("登出")
    @allure.title("登录后登出")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logout(self, logged_in_page, base_url):
        """登录后执行登出"""
        flow = LoginFlow(logged_in_page)
        flow.logout(base_url)
