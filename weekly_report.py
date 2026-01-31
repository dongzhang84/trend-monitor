#!/usr/bin/env python3
"""周报生成入口"""

import argparse
from pathlib import Path

from analyzers import generate_weekly_insights
from reporters import generate_weekly_report
from senders import send_email_report

# 周报保存目录
WEEKLY_REPORT_DIR = Path(__file__).parent / "reports" / "weekly"


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="AI/Tech 趋势周报生成器")
    parser.add_argument("--no-email", action="store_true", help="跳过发送邮件")
    parser.add_argument("--days", type=int, default=7, help="分析最近N天的数据（默认7天）")
    args = parser.parse_args()

    print(f"正在分析最近 {args.days} 天的数据...")

    # 生成分析洞察
    insights = generate_weekly_insights(days=args.days)

    if "error" in insights:
        print(f"❌ 分析失败: {insights['error']}")
        print(f"   {insights.get('message', '')}")
        return

    period = insights["period"]
    days_with_data = period["days_with_data"]
    print(f"  - 数据范围: {period['start']} ~ {period['end']}")
    print(f"  - 有效天数: {days_with_data}")

    if days_with_data < args.days:
        print(f"  ⚠️  数据不足{args.days}天，基于现有{days_with_data}天数据生成周报")

    # 生成周报
    print("正在生成周报...")
    report = generate_weekly_report(insights)

    # 确保目录存在
    WEEKLY_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # 使用周期结束日作为文件名
    end_date = period["end"]
    filename = f"weekly-{end_date}.md"
    file_path = WEEKLY_REPORT_DIR / filename

    # 写入文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ 周报已生成：{file_path}")

    # 发送邮件
    if not args.no_email:
        print("正在发送邮件...")
        if send_email_report(report, subject="AI/Tech 趋势周报"):
            print("✅ 邮件发送成功")
    else:
        print("⏭️  跳过邮件发送")


if __name__ == "__main__":
    main()
