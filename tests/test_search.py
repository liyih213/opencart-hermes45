"""
测试用例: 搜索模块
"""
import allure
import pytest
from flows.search_flow import SearchFlow
from utils.logger import logger


@allure.feature("搜索模块")
class TestSearch:

    @allure.story("有效关键字搜索")
    @allure.title("搜索 'Mac' 应返回相关商品")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize("keyword", ["Mac", "iPhone", "Canon"])
    def test_search_valid_keyword(self, page, base_url, keyword):
        """搜索几个常见关键字 — 结果数 > 0"""
        flow = SearchFlow(page)
        flow.search(base_url, keyword)

    @allure.story("无效关键字搜索")
    @allure.title("搜索不存在的商品应提示无结果")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_invalid_keyword(self, page, base_url, test_data):
        """搜索无效关键字 → 显示 'no product' 提示"""
        keyword = test_data["search"]["invalid_keyword"]
        no_result_text = test_data["search"]["expected_no_result_text"]
        flow = SearchFlow(page)
        flow.search_no_results(base_url, keyword, no_result_text)

    @allure.story("搜索结果进入商品详情")
    @allure.title("搜索 'Mac' 并点击第一条结果进入详情页")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_and_enter_product(self, page, base_url, test_data):
        """搜索结果 → 点击进入商品详情"""
        flow = SearchFlow(page)
        flow.search_and_select_product(base_url, "Mac", product_index=0)
        # 验证页面 URL 包含 product 路由
        assert "product" in page.url.lower() or "product_id" in page.url.lower(), \
            f"未能进入商品详情页，当前 URL: {page.url}"
