"""
Admin 测试 conftest — 独立的 base_url (admin URL)，处理 user_token
"""
import pytest
import re
from utils.config_loader import config as app_config
from pages_admin.admin_login_page import AdminLoginPage


@pytest.fixture(scope="session")
def admin_base_url():
    return app_config.admin_url


@pytest.fixture(scope="session")
def admin_test_data():
    td = app_config.test_data
    return {
        "admin": {"username": "admin", "password": "admin123"},
        **td,
    }


@pytest.fixture(scope="function")
def logged_in_admin_page(page, admin_base_url, admin_test_data):
    """已登录后台的 page，返回 (page, admin_token)"""
    lp = AdminLoginPage(page)
    lp.goto_login(admin_base_url)
    account = admin_test_data["admin"]
    lp.login(account["username"], account["password"])
    lp.assert_login_success()
    # 从 URL 提取 user_token
    url = page.url
    match = re.search(r'user_token=([a-zA-Z0-9]+)', url)
    token = match.group(1) if match else ""
    yield page, token


@pytest.fixture(scope="function")
def admin_page(logged_in_admin_page):
    """简化版：只返回 page"""
    page, _ = logged_in_admin_page
    return page
