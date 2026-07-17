"""
Pytest 全局配置 — fixtures, hooks
"""
import pytest
import allure
from pathlib import Path
from datetime import datetime
from slugify import slugify

from utils.config_loader import config as app_config
from utils.logger import logger
from playwright_stealth.stealth import Stealth
from pages.home_page import HomePage
from pages.login_page import LoginPage


# ═══════════════════════════════════════════════════════════
# 命令行选项
# ═══════════════════════════════════════════════════════════

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="选择测试环境: demo / local (覆盖 settings.yaml 的 active_env)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=None,
        help="无头模式运行",
    )


# ═══════════════════════════════════════════════════════════
# 配置初始化
# ═══════════════════════════════════════════════════════════

def pytest_configure(config):
    """加载 YAML 配置到 pytest 全局"""
    # 处理 --env 参数覆盖
    env_override = config.getoption("--env")
    if env_override:
        _ = app_config.settings  # 触发加载
        app_config._settings["active_env"] = env_override
        logger.info(f"命令行环境覆盖: {env_override}")

    # 将配置注入 pytest namespace
    config.opencart = {
        "base_url": app_config.base_url,
        "browser": app_config.browser_config,
        "screenshot": app_config.screenshot_config,
        "allure": app_config.allure_config,
        "test_data": app_config.test_data,
    }


# ═══════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════

@pytest.fixture(scope="session")
def base_url():
    return app_config.base_url


@pytest.fixture(scope="session")
def admin_base_url():
    return app_config.admin_url


@pytest.fixture(scope="session")
def test_data():
    return app_config.test_data


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    """全局浏览器上下文配置 + 反自动化检测"""
    browser_config = app_config.browser_config

    return {
        **browser_context_args,
        "viewport": {
            "width": browser_config.get("viewport", {}).get("width", 1920),
            "height": browser_config.get("viewport", {}).get("height", 1080),
        },
        "locale": browser_config.get("locale", "en-US"),
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "bypass_csp": True,
        "extra_http_headers": {
            "Accept-Language": "en-US,en;q=0.9",
        },
    }


@pytest.fixture(scope="function")
def page_with_state(page):
    """带自动截图 + 全屏窗口的 page fixture"""
    yield page


@pytest.fixture(scope="function", autouse=True)
def inject_stealth(page):
    """每次新页面自动注入 playwright-stealth 对抗检测"""
    Stealth().apply_stealth_sync(page)
    logger.debug("playwright-stealth 已注入")


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """禁用自动化标志，减少被检测概率"""
    return {
        "args": [
            "--disable-blink-features=AutomationControlled",
        ],
    }


@pytest.fixture
def home_page(page, base_url):
    """首页 Page Object"""
    hp = HomePage(page)
    hp.goto_home(base_url)
    return hp


@pytest.fixture
def login_page(page, base_url):
    """登录页 Page Object"""
    lp = LoginPage(page)
    lp.goto_login(base_url)
    return lp


@pytest.fixture
def logged_in_page(page, base_url, test_data):
    """已登录的 Page（登录后返回首页）"""
    lp = LoginPage(page)
    lp.goto_login(base_url)
    account = test_data["accounts"]["valid"]
    lp.login(account["email"], account["password"])
    # 等待登录跳转完成
    try:
        page.wait_for_url("**account/account**", timeout=10000)
    except Exception:
        page.wait_for_timeout(3000)
    lp.assert_login_success()
    yield page


# ═══════════════════════════════════════════════════════════
# Hooks
# ═══════════════════════════════════════════════════════════

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page") or item.funcargs.get("page_with_state")
        if page:
            # 生成截图路径
            test_name = slugify(item.nodeid.replace("::", "_"))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = Path("reports/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshot_dir / f"{test_name}_{timestamp}.png"

            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
                allure.attach.file(
                    str(screenshot_path),
                    name=f"失败截图: {item.name}",
                    attachment_type=allure.attachment_type.PNG,
                )
                logger.warning(f"失败截图已保存: {screenshot_path}")
            except Exception as e:
                logger.error(f"截图失败: {e}")


def pytest_sessionfinish(session, exitstatus):
    logger.info(f"测试完成，退出码: {exitstatus}")
