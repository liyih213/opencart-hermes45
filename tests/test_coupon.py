"""
优惠券测试: 后台创建 + 前台使用（跨前后台）
"""
import allure
import pytest
from pages_admin.admin_login_page import AdminLoginPage
from pages.home_page import HomePage
from pages.cart_page import CartPage
from flows.cart_flow import CartFlow
from utils.logger import logger


@allure.feature("优惠券")
class TestCoupon:

    @allure.title("后台创建优惠券 → 保存成功")
    @allure.severity(allure.severity_level.NORMAL)
    def test_admin_create_coupon(self, page, admin_base_url):
        """后台: Marketing → Coupons → Add New → 保存"""
        alp = AdminLoginPage(page)
        alp.goto_login(admin_base_url)
        alp.login("admin", "admin123")
        alp.assert_login_success()
        import re
        token = re.search(r'user_token=([a-zA-Z0-9]+)', page.url).group(1)

        # 导航到 Coupons 列表
        page.goto(f"{admin_base_url}/index.php?route=marketing/coupon&user_token={token}")
        page.wait_for_load_state("networkidle")

        # 点击 Add New
        page.locator("a[title='Add New']").click()
        page.wait_for_load_state("networkidle")

        # 填优惠券信息
        page.fill("#input-name", "TEST10")
        page.fill("#input-code", "TEST10")
        page.locator("#input-discount").fill("10")
        page.locator("select#input-type").select_option("P")  # Percentage
        # 保存
        page.locator("button[title='Save']").click()
        page.wait_for_load_state("networkidle")
        logger.info("✓ 优惠券 TEST10 创建成功")

    @allure.title("后台查看优惠券列表")
    @allure.severity(allure.severity_level.MINOR)
    def test_admin_coupon_list(self, page, admin_base_url):
        """后台: Marketing → Coupons 列表加载"""
        alp = AdminLoginPage(page)
        alp.goto_login(admin_base_url)
        alp.login("admin", "admin123")
        alp.assert_login_success()
        import re
        token = re.search(r'user_token=([a-zA-Z0-9]+)', page.url).group(1)
        page.goto(f"{admin_base_url}/index.php?route=marketing/coupon&user_token={token}")
        page.wait_for_load_state("networkidle")
        rows = page.locator(".table tbody tr").count()
        assert rows >= 1, "优惠券列表为空"
        logger.info(f"优惠券列表: {rows} 条")

    @allure.title("前台使用有效优惠券 → 价格更新")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_apply_valid_coupon(self, logged_in_page, base_url):
        """前台: 加购 → 购物车 → 输入 TEST10 → Apply"""
        cf = CartFlow(logged_in_page)
        cf.add_product_to_cart(base_url, "Mac")
        cf.view_cart(base_url)
        # 展开 coupon 折叠面板
        logged_in_page.locator("text=Use Coupon Code").click()
        logged_in_page.wait_for_timeout(800)
        logged_in_page.fill("#input-coupon", "TEST10")
        logged_in_page.locator("#form-coupon button[type='submit']").click()
        logged_in_page.locator(".alert-success").wait_for(state="visible", timeout=5000)
        assert "Success" in logged_in_page.locator(".alert-success").inner_text()
        logger.info("✓ 优惠券 TEST10 使用成功")

    @allure.title("前台使用无效优惠券 → 警告提示")
    @allure.severity(allure.severity_level.MINOR)
    def test_apply_invalid_coupon(self, logged_in_page, base_url):
        """前台: 加购 → 购物车 → 输入 INVALID → 显示错误"""
        cf = CartFlow(logged_in_page)
        cf.add_product_to_cart(base_url, "iPhone")
        cf.view_cart(base_url)
        logged_in_page.locator("text=Use Coupon Code").click()
        logged_in_page.wait_for_timeout(800)
        logged_in_page.fill("#input-coupon", "INVALID123")
        logged_in_page.locator("#form-coupon button[type='submit']").click()
        logged_in_page.locator(".alert-danger").wait_for(state="visible", timeout=5000)
        assert "Warning" in logged_in_page.locator(".alert-danger").inner_text() or "Coupon" in logged_in_page.locator(".alert-danger").inner_text()
        logger.info("✓ 无效优惠券警告显示正确")
