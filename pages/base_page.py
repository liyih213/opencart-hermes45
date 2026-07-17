"""
页面对象基类 — 封装 Playwright Page 通用操作
所有 Page Object 统一继承此类
"""
import allure
from playwright.sync_api import Page, Locator, expect
from utils.logger import logger


# Cloudflare 验证页面特征
CLOUDFLARE_MARKERS = [
    "Just a moment",
    "安全验证",
    "正在检查您的浏览器",
    "Checking your browser",
    "Enable JavaScript",
    "请稍候",
]


class BasePage:
    """页面对象基类"""

    def __init__(self, page: Page):
        self.page = page

    # ── 导航 ──────────────────────────────────────────────

    def _is_cloudflare_challenge(self) -> bool:
        """检测当前页面是否为 Cloudflare 拦截页"""
        try:
            title = self.page.title()
            body = self.page.content()
            for marker in CLOUDFLARE_MARKERS:
                if marker in title or marker in body:
                    return True
        except Exception:
            pass
        return False

    def _wait_for_cloudflare(self, timeout: int = 30000):
        """等待 Cloudflare 验证自动通过并进入真实页面"""
        import time
        deadline = time.time() + timeout / 1000
        while time.time() < deadline:
            if not self._is_cloudflare_challenge():
                logger.info("Cloudflare 验证已通过")
                return True
            time.sleep(1)
        return False

    def navigate(self, url: str, timeout: int = 60000):
        """跳转到指定 URL，自动处理 Cloudflare 挑战"""
        logger.info(f"导航至: {url}")
        with allure.step(f"导航至 {url}"):
            self.page.goto(url, wait_until="domcontentloaded", timeout=timeout)

            # 检测 Cloudflare 拦截并等待
            if self._is_cloudflare_challenge():
                logger.warning("检测到 Cloudflare 验证页面，等待自动通过...")
                passed = self._wait_for_cloudflare(timeout=timeout)
                if passed:
                    self.page.wait_for_load_state("domcontentloaded")
                else:
                    logger.warning(
                        "Cloudflare 验证未在超时时间内通过，"
                        "后续操作可能失败。建议使用本地 OpenCart 实例。"
                    )

    def get_current_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()

    # ── 等待 & 查找 ───────────────────────────────────────

    def wait_for_element(self, selector: str, timeout: int = 15000) -> Locator:
        """等待元素可见并返回"""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def wait_for_url_contains(self, text: str, timeout: int = 15000):
        """等待 URL 包含指定文本"""
        logger.debug(f"等待 URL 包含: {text}")
        self.page.wait_for_url(f"**{text}**", timeout=timeout)

    # ── 元素操作 ──────────────────────────────────────────

    def click(self, selector: str, timeout: int = 15000):
        """点击元素"""
        logger.debug(f"点击: {selector}")
        with allure.step(f"点击 {selector}"):
            self.page.locator(selector).click(timeout=timeout)

    def fill(self, selector: str, text: str, timeout: int = 15000):
        """填充输入框"""
        logger.debug(f"填充 {selector}: {text}")
        with allure.step(f"填充 {selector}"):
            field = self.page.locator(selector)
            field.wait_for(state="visible", timeout=timeout)
            field.fill(text)

    def get_text(self, selector: str, timeout: int = 15000) -> str:
        """获取元素文本"""
        return self.page.locator(selector).inner_text(timeout=timeout)

    def get_element(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """检查元素是否可见"""
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def is_element_present(self, selector: str) -> bool:
        """检查元素是否在 DOM 中"""
        return self.page.locator(selector).count() > 0

    # ── 断言 ──────────────────────────────────────────────

    def assert_text_visible(self, text: str):
        logger.debug(f"断言文本可见: {text}")
        with allure.step(f"验证文本可见: {text}"):
            expect(self.page.get_by_text(text).first).to_be_visible()

    def assert_text_contains(self, selector: str, text: str):
        logger.debug(f"断言 {selector} 包含: {text}")
        with allure.step(f"验证 {selector} 包含 '{text}'"):
            expect(self.page.locator(selector)).to_contain_text(text)

    def assert_url_contains(self, text: str):
        with allure.step(f"验证 URL 包含 '{text}'"):
            assert text in self.page.url, \
                f"URL 不包含 '{text}'，实际: {self.page.url}"

    def assert_element_visible(self, selector: str):
        with allure.step(f"验证元素可见: {selector}"):
            expect(self.page.locator(selector)).to_be_visible()

    # ── 截图 ──────────────────────────────────────────────

    def take_screenshot(self, name: str = "screenshot"):
        path = f"reports/screenshots/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        logger.debug(f"截图已保存: {path}")
