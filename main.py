#!/usr/bin/env python3
"""AI/Tech 趋势监控工具"""

import argparse
from datetime import datetime
from zoneinfo import ZoneInfo

from collectors import fetch_trending_repos, fetch_product_hunt_posts, fetch_hackernews_posts, fetch_ai_tools, fetch_chrome_extensions
from reporters import generate_markdown_report
from senders import send_email_report
from storage import save_daily_data


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="AI/Tech 趋势监控工具")
    parser.add_argument("--no-email", action="store_true", help="跳过发送邮件")
    args = parser.parse_args()

    print("正在采集数据...")

    # 采集Product Hunt
    print("  - 抓取 Product Hunt...")
    products = fetch_product_hunt_posts(limit=5)
    print(f"    获取到 {len(products)} 个产品")

    # 采集There's An AI For That
    print("  - 抓取 There's An AI For That...")
    ai_tools = fetch_ai_tools(limit=5)
    print(f"    获取到 {len(ai_tools)} 个AI工具")

    # 采集Chrome Extensions
    print("  - 抓取 Chrome Extensions...")
    chrome_extensions = fetch_chrome_extensions(limit=5)
    print(f"    获取到 {len(chrome_extensions)} 个扩展")

    # 采集GitHub Trending
    print("  - 抓取 GitHub Trending...")
    repos = fetch_trending_repos(limit=5)
    print(f"    获取到 {len(repos)} 个项目")

    # 采集Hacker News
    print("  - 抓取 Hacker News...")
    hackernews = fetch_hackernews_posts(limit=5)
    print(f"    获取到 {len(hackernews)} 篇文章")

    # 生成报告
    print("正在生成报告...")
    report = generate_markdown_report(repos, products, hackernews, ai_tools, chrome_extensions)

    # 写入文件
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("✅ 报告已生成：report.md")

    # 存储每日数据
    print("正在存储数据...")
    pst = ZoneInfo("America/Los_Angeles")
    today = datetime.now(pst).strftime("%Y-%m-%d")
    daily_data = {
        "product_hunt": products,
        "ai_tools": ai_tools,
        "chrome_extensions": chrome_extensions,
        "github_trending": repos,
        "hacker_news": hackernews,
    }
    if save_daily_data(today, daily_data):
        print(f"✅ 数据已存储：data/daily/{today}.json")
    else:
        print("⚠️  数据存储失败，继续执行...")

    # 发送邮件
    if not args.no_email:
        print("正在发送邮件...")
        if send_email_report(report):
            print("✅ 邮件发送成功")
    else:
        print("⏭️  跳过邮件发送")


if __name__ == "__main__":
    main()
