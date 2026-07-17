#!/usr/bin/env python3
"""
OpenCart UI 自动化测试 — 启动脚本

用法:
    python run_tests.py                  # 默认 demo 环境运行全部
    python run_tests.py --env local      # 本地环境
    python run_tests.py --headless       # 无头模式
    python run_tests.py --smoke          # 只跑冒烟
    python run_tests.py --test test_login  # 指定模块
    python run_tests.py --allure         # 运行后自动生成 Allure 报告
    python run_tests.py --report         # 仅生成报告（不运行测试）
"""
import sys
import os
import subprocess
import argparse
from pathlib import Path

# 确保项目根目录在 PYTHONPATH 中
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


def run_tests(args):
    """运行测试"""
    cmd = ["pytest"]

    # 环境
    if args.env:
        cmd.extend(["--env", args.env])

    # 无头
    if args.headless:
        cmd.append("--headless")

    # 并行
    if args.workers:
        cmd.extend(["-n", str(args.workers)])
    else:
        cmd.extend(["-n", "2"])

    # Allure
    cmd.extend(["--alluredir", "reports/allure-results"])
    if args.clean:
        cmd.append("--clean-alluredir")

    # Test target
    if args.test:
        test_path = f"tests/{args.test}.py"
        if not (PROJECT_ROOT / test_path).exists():
            print(f"错误: 测试文件不存在 — {test_path}")
            sys.exit(1)
        cmd.append(test_path)

    # Markers
    if args.smoke:
        cmd.extend(["-m", "smoke"])
    if args.regression:
        cmd.extend(["-m", "regression"])

    # Verbosity
    if args.quiet:
        cmd.extend(["-q", "--no-header"])
    else:
        cmd.append("-v")

    print(f"\n{'='*60}")
    print(f"  运行命令: {' '.join(cmd)}")
    print(f"{'='*60}\n")

    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    return result.returncode


def generate_allure_report():
    """生成 Allure HTML 报告"""
    results_dir = PROJECT_ROOT / "reports" / "allure-results"
    report_dir = PROJECT_ROOT / "reports" / "allure-report"

    if not list(results_dir.glob("*.json")):
        print("错误: 未找到 allure-results/*.json — 请先运行测试")
        return 1

    print(f"\n生成 Allure 报告 → {report_dir}")
    cmd = [
        "allure", "generate",
        str(results_dir),
        "-o", str(report_dir),
        "--clean",
    ]
    subprocess.run(cmd, cwd=str(PROJECT_ROOT))

    # 尝试打开报告
    print(f"\n✓ 报告已生成: {report_dir}/index.html")
    print(f"  手动打开: allure open {report_dir}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="OpenCart UI 自动化测试启动器"
    )
    parser.add_argument("--env", choices=["demo", "local"], help="测试环境")
    parser.add_argument("--headless", action="store_true", help="无头模式")
    parser.add_argument("--workers", type=int, help="并行 worker 数")
    parser.add_argument("--test", help="指定测试模块 (例: test_login)")
    parser.add_argument("--smoke", action="store_true", help="仅冒烟测试")
    parser.add_argument("--regression", action="store_true", help="仅回归测试")
    parser.add_argument("--clean", action="store_true", help="清理旧 Allure 结果")
    parser.add_argument("--quiet", action="store_true", help="安静模式")
    parser.add_argument("--report", action="store_true", help="仅生成 Allure 报告")
    parser.add_argument("--allure", action="store_true", help="运行 + 生成报告")

    args = parser.parse_args()

    # 仅生成报告
    if args.report:
        sys.exit(generate_allure_report())

    # 运行测试
    exit_code = run_tests(args)

    # 自动生成报告
    if args.allure and exit_code != 2:
        generate_allure_report()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
