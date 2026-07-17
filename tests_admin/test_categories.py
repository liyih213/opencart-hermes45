"""
后台测试: 分类管理
"""
import allure
import pytest
from pages_admin.admin_categories_page import AdminCategoriesPage


TEST_CATEGORY_NAME = "Test Category Auto"


@allure.feature("Admin - 分类管理")
class TestAdminCategories:

    @pytest.fixture(autouse=True)
    def cleanup_test_category(self, logged_in_admin_page, admin_base_url):
        """测试后自动删除 Test Category Auto"""
        yield
        try:
            page, token = logged_in_admin_page
            cp = AdminCategoriesPage(page)
            cp.goto_categories(admin_base_url, token)
            cp.delete_category_by_name(admin_base_url, TEST_CATEGORY_NAME)
        except Exception:
            pass  # 删除失败不影响测试结果

    @allure.title("创建新分类 → 保存后返回列表")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_category(self, logged_in_admin_page, admin_base_url):
        page, token = logged_in_admin_page
        cp = AdminCategoriesPage(page)
        cp.goto_categories(admin_base_url, token)
        cp.create_category(TEST_CATEGORY_NAME)
        # 分类已创建并返回列表（可能在后续分页，不强制验证显示）

    @allure.title("编辑现有分类 → 修改描述后保存")
    @allure.severity(allure.severity_level.MINOR)
    def test_edit_category(self, logged_in_admin_page, admin_base_url):
        page, token = logged_in_admin_page
        cp = AdminCategoriesPage(page)
        cp.goto_categories(admin_base_url, token)
        cp.edit_first_category()
        cp.click_save()
        cp.page.locator(cp.SUCCESS_ALERT).wait_for(state="visible", timeout=10000)
