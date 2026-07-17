"""
Allure 报告增强工具
"""
import allure
from utils.logger import logger


def allure_step(step_name: str):
    """快捷 allure.step 装饰器 + 日志"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.info(f"▶ {step_name}")
            with allure.step(step_name):
                result = func(*args, **kwargs)
            logger.info(f"✓ {step_name} — done")
            return result
        return wrapper
    return decorator


def attach_screenshot(page, name: str = "screenshot"):
    """截图并附加到 Allure 报告"""
    screenshot_bytes = page.screenshot(full_page=True)
    allure.attach(
        screenshot_bytes,
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )
    logger.debug(f"截图已附加: {name}")


def attach_text(content: str, name: str = "detail"):
    """文本附加到 Allure"""
    allure.attach(content, name=name, attachment_type=allure.attachment_type.TEXT)
