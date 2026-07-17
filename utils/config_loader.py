"""
YAML 配置加载器 — 统一读取所有配置文件
"""
import os
import yaml
from pathlib import Path


class ConfigLoader:
    """单例模式配置加载器"""

    _instance = None
    _settings = None
    _test_data = None

    # 项目根目录
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    CONFIG_DIR = PROJECT_ROOT / "config"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def _load_yaml(cls, filename: str) -> dict:
        """加载指定 YAML 文件"""
        filepath = cls.CONFIG_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"配置文件不存在: {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @property
    def settings(self) -> dict:
        """获取 settings 配置"""
        if self._settings is None:
            self._settings = self._load_yaml("settings.yaml")
        return self._settings

    @property
    def test_data(self) -> dict:
        """获取 test_data 配置"""
        if self._test_data is None:
            self._test_data = self._load_yaml("test_data.yaml")
        return self._test_data

    @property
    def active_env(self) -> str:
        return self.settings.get("active_env", "demo")

    @property
    def env_config(self) -> dict:
        """当前激活环境的配置"""
        envs = self.settings.get("environments", {})
        if self.active_env not in envs:
            raise ValueError(f"未找到环境 '{self.active_env}'，可用: {list(envs.keys())}")
        return envs[self.active_env]

    @property
    def base_url(self) -> str:
        return self.env_config.get("base_url", "")

    @property
    def api_url(self) -> str:
        return self.env_config.get("api_url", "")

    @property
    def admin_url(self) -> str:
        return self.env_config.get("admin_url", f"{self.base_url}/admin")

    @property
    def browser_config(self) -> dict:
        return self.settings.get("browser", {})

    @property
    def screenshot_config(self) -> dict:
        return self.settings.get("screenshot", {})

    @property
    def allure_config(self) -> dict:
        return self.settings.get("allure", {})


# 全局实例
config = ConfigLoader()
