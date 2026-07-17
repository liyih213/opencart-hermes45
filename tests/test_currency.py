"""
测试用例: 货币切换
"""
import allure
import pytest
from pages.home_page import HomePage
from utils.logger import logger


@allure.feature("货币切换")
class TestCurrency:

    CURRENCY_TOGGLE = "#form-currency .dropdown-toggle"
    CURRENCY_EURO = "a[href='EUR']"
    CURRENCY_GBP = "a[href='GBP']"

    @allure.story("切换货币为欧元")
    @allure.title("首页切到 Euro → 价格显示 €")
    @allure.severity(allure.severity_level.NORMAL)
    def test_switch_to_euro(self, home_page):
        home_page.page.locator(self.CURRENCY_TOGGLE).click()
        home_page.page.wait_for_timeout(500)
        home_page.page.locator(self.CURRENCY_EURO).click()
        home_page.page.wait_for_load_state("networkidle")
        # 验证价格含 €
        content = home_page.page.content()
        assert "€" in content, "切换到欧元后未找到 € 符号"
        logger.info("✓ 货币已切换到 Euro")

    @allure.story("切换货币为英镑")
    @allure.title("首页切到 GBP → 价格显示 £")
    @allure.severity(allure.severity_level.NORMAL)
    def test_switch_to_gbp(self, home_page):
        home_page.page.locator(self.CURRENCY_TOGGLE).click()
        home_page.page.wait_for_timeout(500)
        home_page.page.locator(self.CURRENCY_GBP).click()
        home_page.page.wait_for_load_state("networkidle")
        content = home_page.page.content()
        assert "£" in content, "切换到英镑后未找到 £ 符号"
        logger.info("✓ 货币已切换到 GBP")
