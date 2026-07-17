"""
Cart Page — 购物车页对象
"""
from pages.base_page import BasePage
from utils.logger import logger


class CartPage(BasePage):
    """OpenCart 购物车页"""

    # ── Selectors ──────────────────────────────────────────
    CART_CONTENT = "#content"
    EMPTY_CART_TEXT = "#content p"
    CART_TABLE = ".table-bordered"
    QUANTITY_INPUTS = "input[name^='quantity']"
    REMOVE_BUTTONS = "button[title='Remove']"
    UPDATE_BUTTON = "button[title='Update']"
    CHECKOUT_BUTTON = "#content a.btn-primary"
    CONTINUE_SHOPPING_BTN = "a.btn-default"
    TOTAL_PRICE = "#content tbody tr:last-child td:last-child"

    # ── Actions ────────────────────────────────────────────

    def goto_cart(self, base_url: str):
        # 保持 URL 一致性，避免 session 丢失
        self.navigate(f"{base_url}/index.php?route=checkout/cart&language=en-gb")
        return self

    def get_cart_items_count(self) -> int:
        """获取购物车中商品种类数"""
        rows = self.page.locator(f"{self.CART_TABLE} tbody tr")
        # 购物车表格最后一行是合计行，减去它
        count = rows.count()
        if count > 0:
            # 最后一行通常是 Total，也有 Remove/Update 按钮的判断
            count = self.page.locator(self.REMOVE_BUTTONS).count()
        return count

    def update_quantity(self, index: int, quantity: int):
        """修改第 N 个商品的购买数量"""
        logger.info(f"修改第 {index + 1} 个商品数量为 {quantity}")
        qty_inputs = self.page.locator(self.QUANTITY_INPUTS)
        qty_inputs.nth(index).fill(str(quantity))
        return self

    def click_update(self):
        self.click(self.UPDATE_BUTTON)
        return self

    def remove_item(self, index: int = 0):
        """移除第 N 个商品"""
        logger.info(f"移除第 {index + 1} 个商品")
        remove_buttons = self.page.locator(self.REMOVE_BUTTONS)
        # dispatch DOM click event 避免可见性检查
        remove_buttons.nth(index).dispatch_event("click")
        self.page.wait_for_load_state("networkidle")
        return self

    def click_checkout(self):
        logger.info("去结账")
        self.click(self.CHECKOUT_BUTTON)
        return self

    # ── Assertions ─────────────────────────────────────────

    def assert_cart_not_empty(self):
        count = self.get_cart_items_count()
        assert count > 0, "购物车为空！"
        logger.info(f"购物车中有 {count} 种商品")

    def assert_cart_empty(self):
        """断言购物车为空"""
        self.wait_for_element(self.EMPTY_CART_TEXT)
        text = self.get_text(self.EMPTY_CART_TEXT)
        logger.info(f"购物车提示: {text}")
        assert "empty" in text.lower() or "空" in text, f"购物车非空: {text}"

    def assert_quantity_is(self, index: int, expected: int):
        qty_inputs = self.page.locator(self.QUANTITY_INPUTS)
        actual = qty_inputs.nth(index).input_value()
        assert actual == str(expected), \
            f"数量不匹配: 期望 {expected}, 实际 {actual}"
