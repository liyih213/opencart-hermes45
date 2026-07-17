"""
Product Page — 商品详情页对象
"""
from pages.base_page import BasePage
from utils.logger import logger


class ProductPage(BasePage):
    """OpenCart 商品详情页"""

    # ── Selectors ──────────────────────────────────────────
    PRODUCT_NAME = "#content h1"
    PRODUCT_PRICE = "#content h2"  # OpenCart 商品详情页价格通常在一个独立的 h2 或 span 中
    PRICE_NEW = ".price-new"       # 特价标签
    PRICE_OLD = ".price-old"       # 原价标签
    QUANTITY_INPUT = "#input-quantity"
    ADD_TO_CART_BUTTON = "#button-cart"
    CART_SUCCESS_ALERT = ".alert-success"

    # ── Actions ────────────────────────────────────────────

    def get_product_name(self) -> str:
        name = self.get_text(self.PRODUCT_NAME)
        logger.debug(f"商品名称: {name}")
        return name

    def get_product_price(self) -> str:
        """尝试获取商品价格（优先 .price-new，其次 h2 中的价格文本）"""
        try:
            price = self.get_text(self.PRICE_NEW)
        except Exception:
            # fallback: 获取包含 $ 符号的 h2 文本
            locator = self.page.locator(self.PRODUCT_PRICE)
            price = locator.inner_text()
        logger.debug(f"商品价格: {price}")
        return price.strip()

    def set_quantity(self, quantity: int):
        """设置购买数量"""
        logger.debug(f"设置数量: {quantity}")
        self.fill(self.QUANTITY_INPUT, str(quantity))
        return self

    def click_add_to_cart(self):
        """点击加入购物车"""
        logger.info("加入购物车")
        self.click(self.ADD_TO_CART_BUTTON)
        return self

    def add_to_cart(self, quantity: int = 1):
        """完整「加入购物车」流程"""
        if quantity != 1:
            self.set_quantity(quantity)
        self.click_add_to_cart()
        return self

    # ── Assertions ─────────────────────────────────────────

    def assert_add_to_cart_success(self):
        """断言加入购物车成功"""
        self.wait_for_element(self.CART_SUCCESS_ALERT)
        alert_text = self.get_text(self.CART_SUCCESS_ALERT)
        logger.info(f"加入购物车成功: {alert_text}")

    def assert_product_name_contains(self, keyword: str):
        name = self.get_product_name()
        assert keyword.lower() in name.lower(), \
            f"商品名称 '{name}' 不包含 '{keyword}'"
