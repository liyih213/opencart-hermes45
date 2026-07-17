# OpenCart UI 自动化测试框架

![Tests](https://img.shields.io/badge/tests-32%20passed-brightgreen)
![Browsers](https://img.shields.io/badge/browsers-Chromium%20%7C%20Firefox%20%7C%20WebKit-blue)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF)
![Python](https://img.shields.io/badge/python-3.12-3776AB)
![Playwright](https://img.shields.io/badge/playwright-1.61-45ba4b)

**POM 三层架构 | 多浏览器并行 | YAML 配置驱动 | Allure 报告 | GitHub Actions CI**

```
                  ┌──────────────────────────────┐
                  │        Test Layer             │
                  │  32 条 × 3 browsers = 96 条   │
                  │  smoke (7条) + full (96条)    │
                  └─────────────┬────────────────┘
                                │
                  ┌─────────────▼────────────────┐
                  │        Flow Layer             │
                  │  Login / Search / Cart /      │
                  │  Checkout / Coupon            │
                  └─────────────┬────────────────┘
                                │
                  ┌─────────────▼────────────────┐
                  │      Page Object Layer        │
                  │  13 个 PO (前台 8 + 后台 5)    │
                  │  BasePage 基类                 │
                  └─────────────┬────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
   config/settings.yaml   utils/logger.py      .github/workflows/
   config/test_data.yaml  utils/allure.py      ci.yml (smoke+full)
```

## 快速开始

```bash
pip install -r requirements.txt
python -m playwright install chromium firefox webkit

# 全量 (3 browsers, 96 条)
python -m pytest tests/ tests_admin/ -v -n 4 --browser chromium --browser firefox --browser webkit

# 冒烟 (7 条, 30s)
python -m pytest tests/ tests_admin/ -v -m smoke -n 4

# 单浏览器
python -m pytest tests/ tests_admin/ -v -k chromium
```

## 覆盖矩阵 (32 条 / browser)

| 模块 | 用例 | smoke |
|------|------|:-----:|
| Login | 正确登录 / 错误登录 / 登出 | ✅ |
| Navigation | 首页 / 搜索栏 / 3 个分类导航 | ✅ |
| Search | 3 关键字 / 无结果 / 进入详情 | ✅ |
| Cart | 加购 / 改数量 / 移除 / 空购物车 | ✅ |
| Checkout | 完整结账 (Shipping → Payment → Confirm) | ✅ |
| Currency | EUR € / GBP £ | |
| Admin | 登录 / 商品列表+搜索 / 订单列表+详情 / 分类增+改 | |
| Coupon | 后台创建+列表 / 前台使用+无效 | |

## CI/CD

| 触发 | Job | 内容 |
|------|-----|------|
| `git push` | **smoke** | 7 条 smoke，4 workers，30s |
| PR merge | **full** | 96 条 (3 browsers)，14 workers，~3min |
| 手动 | both | workflow_dispatch |

报告自动部署到 GitHub Pages。

## 技术栈

Python 3.12 · Playwright · Pytest · pytest-xdist · pytest-rerunfailures · Allure · YAML · GitHub Actions · playwright-stealth
