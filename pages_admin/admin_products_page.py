"""
Admin Products Page — 商品管理
"""
from pages.base_page import BasePage
from utils.logger import logger


class AdminProductsPage(BasePage):
    """后台商品列表"""

    PRODUCT_TABLE = ".table"
    SEARCH_NAME = "#input-name"
    FILTER_BUTTON = "#button-filter"
    PRODUCT_ROWS = "form#form-product tbody tr"

    def goto_products(self, admin_url: str, token: str = ""):
        url = f"{admin_url}/index.php?route=catalog/product"
        if token:
            url += f"&user_token={token}"
        self.navigate(url)
        self.page.wait_for_load_state("networkidle")
        # 等待 AJAX 产品列表加载
        self.page.locator("form#form-product tbody tr").first.wait_for(state="visible", timeout=15000)
        return self

    def search_product(self, name: str):
        logger.info(f"后台搜索商品: {name}")
        self.fill(self.SEARCH_NAME, name)
        self.click(self.FILTER_BUTTON)
        self.page.wait_for_load_state("networkidle")
        return self

    def get_product_count(self) -> int:
        """获取产品行数（排除 th 表头行）"""
        return self.page.locator(self.PRODUCT_ROWS).count()

    def assert_products_listed(self, min_count: int = 1):
        count = self.get_product_count()
        assert count >= min_count, f"商品列表不足: 期望≥{min_count}, 实际{count}"
        logger.info(f"商品列表: {count} 条")
