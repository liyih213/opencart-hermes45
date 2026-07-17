# OpenCart UI 自动化测试框架

**Python + Playwright + Pytest + Allure | 32 条用例 | POM 三层架构 | YAML 配置驱动**

---

## 项目概述

为 OpenCart 4.x 电商平台构建的全栈 UI 自动化测试框架，覆盖**前台商城**（Storefront）与**后台管理系统**（Admin）两大模块，实现从商品浏览、搜索、购物车、结账到后台商品管理、订单管理、优惠券管理的全链路自动化验证。

## 技术栈

| 层级 | 技术 |
|------|------|
| 语言 | Python 3.12 |
| 浏览器驱动 | Playwright (Chromium) |
| 测试框架 | Pytest + pytest-xdist + pytest-rerunfailures |
| 报告 | Allure Report |
| 配置管理 | YAML 配置驱动（多环境 + 测试数据分离） |
| 反检测 | playwright-stealth + 自定义 UA + AutomationControlled 禁用 |
| 架构模式 | POM 三层架构（Pages → Flows → Tests） |

## 架构设计

```
┌─────────────────────────────────────────────┐
│                  Test Layer                  │
│  tests/ (21 条前台) + tests_admin/ (7 条后台)  │
│  独立 conftest.py 管理 fixture 作用域          │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│                Flow Layer                    │
│  flows/ (4 个) + flows_admin/               │
│  组合 Page Object 形成业务场景                │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│               Page Object Layer              │
│  pages/ (8 个前台) + pages_admin/ (5 个后台)  │
│  BasePage 基类封装通用 wait/click/fill/assert  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│              Infrastructure                  │
│  config/ YAML + utils/ 日志/Allure + pytest  │
└─────────────────────────────────────────────┘
```

## 测试覆盖矩阵 (32/32 PASS)

### 前台 Storefront — 21 条

| 模块 | 用例数 | 覆盖场景 |
|------|--------|----------|
| Login | 3 | 正确登录 / 错误登录 / 登出 |
| Navigation | 5 | 首页加载 / 搜索栏 / 3 个分类导航 |
| Search | 5 | 3 关键字搜索 / 无结果 / 进入详情 |
| Cart | 5 | 加购 / 改数量 / 移除清空 / 空购物车 |
| Checkout | 1 | 完整结账 (Address → Flat Rate → COD → Confirm) |
| Currency | 2 | 切换 EUR € / GBP £ |

### 后台 Admin — 7 条

| 模块 | 用例数 | 覆盖场景 |
|------|--------|----------|
| Admin Login | 1 | admin 登录 → Dashboard |
| Products | 2 | 商品列表 (10条) / 搜索 MacBook |
| Orders | 2 | 订单列表 (10条) / 查看详情 |
| Categories | 2 | 创建分类 / 编辑分类 |

### 优惠券 — 4 条 (跨前后台)

| 模块 | 用例数 | 覆盖场景 |
|------|--------|----------|
| Coupon Admin | 2 | 后台创建 TEST10 / 查看列表 |
| Coupon Front | 2 | 前台使用有效券 → 折扣生效 / 无效券 → 警告 |

## 关键技术实现

- **CSRF Token 自动提取**: Admin 页面 URL 含 `user_token`，conftest 从登录重定向中提取并注入后续请求
- **Cloudflare 挑战自适应等待**: BasePage.navigate() 自动检测 Cloudflare 拦截页并轮询等待
- **Bootstrap 组件适配**: 处理 radio/checkbox 隐藏问题（`dispatch_event("click")` 替代 click）
- **多环境切换**: `--env local/demo` 命令行参数动态切换配置
- **失败自动截图**: `pytest_runtest_makereport` hook 实现失败时的全页截图 + Allure 附件
- **管理员 session 销毁与重建**: 防止测试数据污染，支持 create → verify → cleanup 流程

## 运行方式

```bash
# 全量 32 条
python -m pytest tests/ tests_admin/ -v --alluredir=reports/allure-results

# 单模块
python -m pytest tests/test_login.py -v

# 生成 Allure 报告
allure generate reports/allure-results -o reports/allure-report --clean && allure open reports/allure-report
```

## 项目规模

| 指标 | 数值 |
|------|------|
| 测试用例 | 32 条 (全 PASS) |
| Page Object 文件 | 13 个 |
| Flow 文件 | 4 个 |
| 配置文件 | 2 个 YAML |
| 总执行时间 | ~138s (串行) |
| Python 源文件 | 25+ |
