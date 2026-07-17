"""
日志工具 — 统一的日志输出
"""
import logging
import sys
from pathlib import Path
from datetime import datetime


def get_logger(name: str = "opencart_ui") -> logging.Logger:
    """获取 logger 实例"""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # 控制台 handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_fmt = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(message)s",
            datefmt="%H:%M:%S",
        )
        console_handler.setFormatter(console_fmt)
        logger.addHandler(console_handler)

        # 文件 handler
        log_dir = Path(__file__).resolve().parent.parent / "reports" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_fmt = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(file_fmt)
        logger.addHandler(file_handler)

    return logger


# 模块级 logger
logger = get_logger()
