"""Markdown 报告生成器"""

from datetime import datetime
from zoneinfo import ZoneInfo


def generate_markdown_report(repos, products, hackernews_posts, ai_tools=None, chrome_extensions=None):
    """生成Markdown格式的报告"""
    pst = ZoneInfo("America/Los_Angeles")
    now = datetime.now(pst)
    tz_abbr = now.strftime("%Z")  # PST 或 PDT（自动处理夏令时）
    timestamp = now.strftime(f"%Y-%m-%d %H:%M ({tz_abbr})")

    lines = [
        "# AI/Tech 趋势日报",
        "",
        f"**生成时间**: {timestamp}",
        "",
        "---",
        "",
        "## Product Hunt 今日热门",
        "",
    ]

    if products:
        for i, product in enumerate(products, 1):
            lines.append(f"### {i}. [{product['name']}]({product['link']})")
            lines.append("")
            lines.append(f"- **简介**: {product['tagline']}")
            lines.append("")
    else:
        lines.append("*暂无数据*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## There's An AI For That - 今日新工具")
    lines.append("")

    if ai_tools:
        for i, tool in enumerate(ai_tools, 1):
            lines.append(f"### {i}. [{tool['name']}]({tool['link']})")
            lines.append("")
            lines.append(f"- **描述**: {tool['description']}")
            lines.append(f"- **分类**: {tool['category']}")
            lines.append("")
    else:
        lines.append("*暂无数据*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Chrome Extensions 热门")
    lines.append("")

    if chrome_extensions:
        for i, ext in enumerate(chrome_extensions, 1):
            lines.append(f"### {i}. [{ext['name']}]({ext['link']})")
            lines.append("")
            lines.append(f"- **描述**: {ext['description']}")
            lines.append(f"- **安装量**: {ext['users']} | **评分**: {ext['rating']}")
            lines.append("")
    else:
        lines.append("*暂无数据*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## GitHub Trending")
    lines.append("")

    if repos:
        for i, repo in enumerate(repos, 1):
            lines.append(f"### {i}. [{repo['name']}](https://github.com/{repo['name']})")
            lines.append("")
            lines.append(f"- **描述**: {repo['description']}")
            lines.append(f"- **今日Stars**: {repo['today_stars']}")
            lines.append("")
    else:
        lines.append("*暂无数据*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Hacker News 热门")
    lines.append("")

    if hackernews_posts:
        for i, post in enumerate(hackernews_posts, 1):
            lines.append(f"### {i}. [{post['title']}]({post['url']})")
            lines.append("")
            lines.append(f"- **作者**: {post['author']}")
            lines.append(f"- **分数**: {post['score']} points | **评论**: {post['comments']}")
            lines.append("")
    else:
        lines.append("*暂无数据*")
        lines.append("")

    return "\n".join(lines)
