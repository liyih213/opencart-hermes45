"""
Search Results Page — 搜索结果页对象
"""
from pages.base_page import BasePage
from utils.logger import logger


class SearchResultsPage(BasePage):
    """OpenCart 搜索结果页"""

    # ── Selectors ──────────────────────────────────────────
    SEARCH_HEADING = "#content h1"
    PRODUCT_ITEMS = ".product-thumb"
    PRODUCT_NAMES = ".product-thumb h4 a"
    NO_RESULTS_TEXT = "#content p"
    SORT_DROPDOWN = "#input-sort"
    GRID_VIEW_BUTTON = "#grid-view"
    LIST_VIEW_BUTTON = "#list-view"

    # ── Actions ────────────────────────────────────────────

    def get_results_count(self) -> int:
        return self.page.locator(self.PRODUCT_ITEMS).count()

    def get_result_names(self) -> list[str]:
        """获取所有搜索结果名称"""
        names = self.page.locator(self.PRODUCT_NAMES).all_inner_texts()
        return [n.strip() for n in names]

    def click_product_by_index(self, index: int = 0):
        """点击第 N 个搜索结果"""
        logger.info(f"点击第 {index + 1} 个搜索结果")
        self.page.locator(self.PRODUCT_NAMES).nth(index).click()
        return self

    def click_product_by_name(self, name: str):
        """根据名称点击商品"""
        logger.info(f"点击商品: {name}")
        self.click(f"text={name}")
        return self

    # ── Assertions ─────────────────────────────────────────

    def assert_results_displayed(self, min_count: int = 1):
        count = self.get_results_count()
        assert count >= min_count, f"期望至少 {min_count} 条结果，实际 {count} 条"
        logger.info(f"搜索结果数: {count}")

    def assert_no_results(self, expected_text: str | None = None):
        assert self.get_results_count() == 0, "期望无搜索结果，但实际有结果"
        if expected_text:
            no_result = self.get_text(self.NO_RESULTS_TEXT)
            assert expected_text in no_result, \
                f"期望提示 '{expected_text}'，实际 '{no_result}'"
        logger.info("搜索结果为空 — 符合预期")

    def assert_results_contain(self, keyword: str):
        names = self.get_result_names()
        for name in names:
            assert keyword.lower() in name.lower(), \
                f"商品 '{name}' 不包含关键字 '{keyword}'"
        logger.info(f"所有 {len(names)} 条结果均包含 '{keyword}'")
