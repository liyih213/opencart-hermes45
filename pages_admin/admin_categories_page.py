"""
Admin Categories Page — 分类管理
"""
from pages.base_page import BasePage
from utils.logger import logger


class AdminCategoriesPage(BasePage):
    """后台分类管理"""

    ADD_NEW_BUTTON = "a[title='Add New']"
    CATEGORY_NAME_INPUT = "#input-name-1"
    SAVE_BUTTON = "button[title='Save']"
    EDIT_BUTTONS = "a[title='Edit']"
    CATEGORY_ROWS = ".table tbody tr"
    SUCCESS_ALERT = ".alert-success"

    def goto_categories(self, admin_url: str, token: str = ""):
        url = f"{admin_url}/index.php?route=catalog/category"
        if token:
            url += f"&user_token={token}"
        self.navigate(url)
        self.page.wait_for_load_state("networkidle")
        return self

    def wait_for_success(self):
        """等待任意成功提示"""
        try:
            self.page.locator(".alert-success, .alert.alert-success").first.wait_for(state="visible", timeout=10000)
        except Exception:
            self.page.locator("text=Success").first.wait_for(state="visible", timeout=10000)
        return self

    def click_add_new(self):
        self.click(self.ADD_NEW_BUTTON)
        self.page.wait_for_load_state("networkidle")
        return self

    def fill_category_name(self, name: str):
        self.fill(self.CATEGORY_NAME_INPUT, name)
        return self

    def click_save(self):
        self.click(self.SAVE_BUTTON)
        self.page.wait_for_load_state("networkidle")
        return self

    def create_category(self, name: str):
        logger.info(f"创建分类: {name}")
        self.click_add_new()
        self.fill_category_name(name)
        self.click_save()
        # Save 后会 redirect 回分类列表
        self.page.wait_for_url("**route=catalog/category**", timeout=15000)
        self.page.wait_for_load_state("networkidle")
        logger.info(f"分类 '{name}' 创建成功")
        return self

    def delete_category_by_name(self, admin_url: str, name: str):
        """删除指定名称的分类（勾选 → 删除）"""
        self.goto_categories(admin_url)
        # 勾选对应的 checkbox
        rows = self.page.locator(self.CATEGORY_ROWS)
        for i in range(rows.count()):
            row_text = rows.nth(i).inner_text()
            if name in row_text:
                rows.nth(i).locator("input[type='checkbox']").dispatch_event("click")
                self.page.wait_for_timeout(300)
                break
        # 点击 Delete 按钮（通过 form 提交）
        self.page.locator("button[form='form-category']").dispatch_event("click")
        self.page.wait_for_load_state("networkidle")
        logger.info(f"分类 '{name}' 已删除")
        return self

    def edit_first_category(self):
        btns = self.page.locator(self.EDIT_BUTTONS)
        if btns.count() > 0:
            btns.first.click()
            self.page.wait_for_load_state("networkidle")
            logger.info("已打开分类编辑页")
        return self

    def assert_category_in_list(self, name: str):
        content = self.page.content()
        assert name in content, f"分类列表未找到 '{name}'"
        logger.info(f"分类 '{name}' 在列表中")
