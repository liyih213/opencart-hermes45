"""
Home Page — 首页对象
"""
from pages.base_page import BasePage
from utils.logger import logger


class HomePage(BasePage):
    """OpenCart 首页"""

    # ── Selectors ──────────────────────────────────────────
    SEARCH_INPUT = "input[name='search']"
    SEARCH_BUTTON = "#search button[type='button']"
    CART_TOTAL = "#header-cart button"
    CART_BUTTON = "#header-cart button"
    CART_VIEW_LINK = "text=View Cart"
    MY_ACCOUNT_DROPDOWN = "a[title='My Account']"
    MY_ACCOUNT_LOGIN = "text=Login"
    MY_ACCOUNT_REGISTER = "text=Register"
    FEATURED_PRODUCTS = ".product-thumb"
    TOP_NAV = "#menu"
    CURRENCY_DROPDOWN = "#form-currency"

    # ── Actions ────────────────────────────────────────────

    def goto_home(self, base_url: str):
        """打开首页"""
        self.navigate(base_url)
        return self

    def search(self, keyword: str):
        """搜索商品"""
        logger.info(f"搜索: {keyword}")
        self.fill(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state("networkidle")
        # Firefox/WebKit 可能需要额外等待 AJAX 渲染
        self.page.wait_for_timeout(500)
        return self

    def open_cart_dropdown(self):
        self.click(self.CART_BUTTON)
        return self

    def go_to_cart(self):
        self.open_cart_dropdown()
        self.click(self.CART_VIEW_LINK)
        return self

    def open_my_account_menu(self):
        self.click(self.MY_ACCOUNT_DROPDOWN)
        return self

    def go_to_login(self):
        self.open_my_account_menu()
        self.click(self.MY_ACCOUNT_LOGIN)
        return self

    def go_to_register(self):
        self.open_my_account_menu()
        self.click(self.MY_ACCOUNT_REGISTER)
        return self

    def click_top_category(self, category_name: str):
        """点击顶部导航分类"""
        logger.info(f"导航分类: {category_name}")
        # 使用 navbar 范围内的精确文本匹配，避免匹配 "Show All xxx" 等
        self.page.locator("nav").get_by_role("link", name=category_name).first.click()
        return self

    def get_featured_products_count(self) -> int:
        """获取首页推荐商品数量"""
        return self.page.locator(self.FEATURED_PRODUCTS).count()

    # ── Assertions ─────────────────────────────────────────

    def assert_on_homepage(self):
        self.assert_text_visible("Featured")
        logger.debug("已确认在首页")

    def assert_search_bar_visible(self):
        self.assert_element_visible(self.SEARCH_INPUT)

    def assert_featured_products_displayed(self):
        count = self.get_featured_products_count()
        assert count > 0, "首页未显示任何推荐商品"
        logger.info(f"首页显示 {count} 个推荐商品")
