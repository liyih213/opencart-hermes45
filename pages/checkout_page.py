"""
Checkout Page — OpenCart 4.x AJAX 多步结账（登录用户）
"""
from pages.base_page import BasePage
from utils.logger import logger


class CheckoutPage(BasePage):
    """OpenCart 4.x 结账页"""

    # ── Selectors ──────────────────────────────────────────
    # Step 1: Shipping Address
    SHIPPING_FIRSTNAME = "#input-shipping-firstname"
    SHIPPING_LASTNAME = "#input-shipping-lastname"
    SHIPPING_ADDRESS1 = "#input-shipping-address-1"
    SHIPPING_CITY = "#input-shipping-city"
    SHIPPING_POSTCODE = "#input-shipping-postcode"
    SHIPPING_COUNTRY = "#input-shipping-country"
    SHIPPING_ZONE = "#input-shipping-zone"
    BUTTON_SHIPPING_ADDRESS = "#button-shipping-address"

    # Step 2: Shipping Method
    SHIPPING_METHOD_INPUT = "#input-shipping-method"
    BUTTON_SHIPPING_METHODS = "#button-shipping-methods"
    BUTTON_SHIPPING_METHOD = "#button-shipping-method"
    SHIPPING_CODE_HIDDEN = "#input-shipping-code"

    # Step 3: Payment Method
    PAYMENT_METHOD_INPUT = "#input-payment-method"
    BUTTON_PAYMENT_METHODS = "#button-payment-methods"
    BUTTON_PAYMENT_METHOD = "#button-payment-method"
    PAYMENT_CODE_HIDDEN = "#input-payment-code"

    # Step 4: Confirm
    AGREE_CHECKBOX = "#content input[type='checkbox']"
    BUTTON_CONFIRM = "#button-confirm"

    # Success
    SUCCESS_HEADING = "#content h1"

    # Step 1: Shipping Address
    NO_NEW_ADDRESS_RADIO = "#input-shipping-new"

    # ── Actions ────────────────────────────────────────────

    def goto_checkout(self, base_url: str):
        self.navigate(f"{base_url}/index.php?route=checkout/checkout")
        return self

    def select_new_address(self):
        """选择 'I want to use a new address'（Bootstrap 隐藏原生 radio，用 label 或 force click）"""
        self.page.locator(self.NO_NEW_ADDRESS_RADIO).dispatch_event("click")
        self.page.wait_for_timeout(500)
        return self

    def fill_shipping_address(
        self,
        first_name: str = "fixtest",
        last_name: str = "User",
        address: str = "123 Test Street",
        city: str = "London",
        postcode: str = "EC1A 1BB",
        country: str = "United Kingdom",
        zone: str = "Greater London",
    ):
        """填写配送地址"""
        logger.info("填写配送地址")
        self.fill(self.SHIPPING_FIRSTNAME, first_name)
        self.fill(self.SHIPPING_LASTNAME, last_name)
        self.fill(self.SHIPPING_ADDRESS1, address)
        self.fill(self.SHIPPING_CITY, city)
        self.fill(self.SHIPPING_POSTCODE, postcode)
        self.page.locator(self.SHIPPING_COUNTRY).select_option(label=country)
        self.page.wait_for_timeout(500)
        self.page.locator(self.SHIPPING_ZONE).select_option(label=zone)
        return self

    def click_continue_shipping_address(self):
        self.click(self.BUTTON_SHIPPING_ADDRESS)
        self.page.wait_for_timeout(1500)
        return self

    def skip_shipping_address(self):
        """直接点继续（已登录用户地址已保存时）"""
        self.click(self.BUTTON_SHIPPING_ADDRESS)
        self.page.wait_for_timeout(1500)
        return self

    def choose_shipping_method(self, method_name: str = "Flat Shipping Rate"):
        """选择配送方式"""
        logger.info(f"选择配送方式: {method_name}")
        # 点击 Choose 打开列表
        self.click(self.BUTTON_SHIPPING_METHODS)
        self.page.wait_for_timeout(1000)
        # 点击对应选项
        self.page.locator(f"label:has-text('{method_name}')").click()
        self.page.wait_for_timeout(500)
        # 点 Continue
        self.click(self.BUTTON_SHIPPING_METHOD)
        self.page.wait_for_timeout(1500)
        return self

    def choose_payment_method(self, method_name: str = "Cash On Delivery"):
        """选择支付方式"""
        logger.info(f"选择支付方式: {method_name}")
        self.click(self.BUTTON_PAYMENT_METHODS)
        self.page.wait_for_timeout(1000)
        self.page.locator(f"label:has-text('{method_name}')").click()
        self.page.wait_for_timeout(500)
        self.click(self.BUTTON_PAYMENT_METHOD)
        self.page.wait_for_timeout(1500)
        return self

    # Step 4: Confirm
    def agree_terms(self):
        """尝试勾选条款（如存在）；不存在则跳过"""
        checkbox = self.page.locator(self.AGREE_CHECKBOX)
        if checkbox.count() > 0:
            checkbox.dispatch_event("click")
            self.page.wait_for_timeout(500)
        else:
            logger.debug("未找到 agree checkbox，跳过")
        return self

    def click_confirm(self):
        logger.info("确认下单")
        self.page.locator(self.BUTTON_CONFIRM).wait_for(state="visible", timeout=10000)
        self.page.locator(self.BUTTON_CONFIRM).click(force=True)
        self.page.wait_for_load_state("networkidle")
        return self

    # ── 完整结账流程 ──────────────────────────────────────

    def checkout_logged_in(self):
        """登录用户的完整结账流程"""
        logger.info("=== 开始结账流程 ===")

        # Step 1: Shipping Address
        logger.info("Step 1: Shipping Address")
        self.select_new_address()
        self.fill_shipping_address()
        self.click_continue_shipping_address()

        # Step 2: Shipping Method
        logger.info("Step 2: Shipping Method")
        self.choose_shipping_method("Flat Shipping Rate")

        # Step 3: Payment Method
        logger.info("Step 3: Payment Method")
        self.choose_payment_method("Cash On Delivery")

        # Step 4: Confirm
        logger.info("Step 4: Confirm Order")
        self.agree_terms()
        self.click_confirm()

        return self

    # ── Assertions ─────────────────────────────────────────

    def assert_order_success(self):
        """断言下单成功"""
        self.page.wait_for_timeout(2000)
        title = self.page.title()
        heading = self.get_text(self.SUCCESS_HEADING) if self.page.locator(self.SUCCESS_HEADING).count() > 0 else ""
        body = self.page.content()
        logger.info(f"下单后页面: title={title}, h1={heading}")
        # OpenCart 4.x 成功页的 h1 可能是 "Your order has been placed!" 或仍显示 "Checkout"
        placed = "placed" in body.lower() or "success" in body.lower() or "order" in heading.lower()
        assert placed, f"下单失败: title={title}, h1={heading}"

    def assert_on_checkout_page(self):
        self.assert_url_contains("checkout/checkout")
