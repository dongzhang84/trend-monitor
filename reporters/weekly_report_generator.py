"""周报生成器"""

from datetime import datetime
from zoneinfo import ZoneInfo


def generate_weekly_report(insights):
    """
    基于分析结果生成格式化的Markdown周报

    Args:
        insights: generate_weekly_insights() 返回的分析结果

    Returns:
        str: Markdown格式的周报内容
    """
    # 检查错误
    if "error" in insights:
        return f"# 周报生成失败\n\n{insights.get('message', '数据不足')}"

    # 获取时间信息
    period = insights["period"]
    pst = ZoneInfo("America/Los_Angeles")
    now = datetime.now(pst)
    tz_abbr = now.strftime("%Z")
    generated_time = now.strftime(f"%Y-%m-%d %H:%M ({tz_abbr})")

    lines = [
        "# AI/Tech 趋势周报",
        "",
        f"**统计周期**: {period['start']} 至 {period['end']} (共{period['days_with_data']}天数据)",
        f"**生成时间**: {generated_time}",
        "",
        "---",
        "",
    ]

    # 数据概览
    lines.extend(_generate_overview(insights))

    # 热门关键词
    lines.extend(_generate_keywords_section(insights))

    # 重复出现（持续热度）
    lines.extend(_generate_repeated_section(insights))

    # 本周新发现
    lines.extend(_generate_new_discoveries_section(insights))

    # 分类统计
    lines.extend(_generate_statistics_section(insights))

    # 页脚
    lines.append("---")
    lines.append("")
    lines.append("*周报由 Trend Monitor 自动生成*")
    lines.append("")

    return "\n".join(lines)


def _generate_overview(insights):
    """生成数据概览部分"""
    lines = [
        "## 本周数据概览",
        "",
    ]

    source_names = {
        "product_hunt": "Product Hunt",
        "ai_tools": "AI 工具",
        "chrome_extensions": "Chrome 扩展",
        "github_trending": "GitHub 项目",
        "hacker_news": "Hacker News",
    }

    total_count = 0
    for source_key in source_names:
        source_data = insights.get(source_key, {})
        total_count += source_data.get("total", 0)

    lines.append(f"- **监测条目总数**: {total_count:,} 个")
    lines.append("")

    for source_key, name in source_names.items():
        source_data = insights.get(source_key, {})
        count = source_data.get("total", 0)
        unique = source_data.get("unique", 0)
        lines.append(f"- {name}: {count} 个 (去重后 {unique} 个)")

    lines.append("")
    lines.append("---")
    lines.append("")

    return lines


def _generate_keywords_section(insights):
    """生成热门关键词部分"""
    lines = [
        "## 本周热门关键词",
        "",
    ]

    keywords = insights.get("keywords", [])
    if keywords:
        for i, (word, count) in enumerate(keywords[:10], 1):
            lines.append(f"{i}. **{word}** - 出现 {count} 次")
    else:
        lines.append("*本周暂无关键词数据*")

    lines.append("")
    lines.append("---")
    lines.append("")

    return lines


def _generate_repeated_section(insights):
    """生成重复出现（持续热度）部分"""
    lines = [
        "## 重复出现（持续热度）",
        "",
        "*以下产品/工具在本周多次出现，值得重点关注：*",
        "",
    ]

    source_config = [
        ("product_hunt", "Product Hunt", "tagline"),
        ("ai_tools", "AI 工具", "description"),
        ("chrome_extensions", "Chrome 扩展", "description"),
        ("github_trending", "GitHub 项目", "description"),
        ("hacker_news", "Hacker News", None),
    ]

    has_any_repeated = False

    for source_key, section_name, desc_field in source_config:
        source_data = insights.get(source_key, {})
        repeated = source_data.get("repeated", [])

        lines.append(f"### {section_name}")
        lines.append("")

        if repeated:
            has_any_repeated = True
            for i, item_data in enumerate(repeated[:5], 1):
                item = item_data["item"]
                count = item_data["count"]
                first_seen = _format_date(item_data["first_seen"])
                last_seen = _format_date(item_data["last_seen"])

                name = item.get("name") or item.get("title", "Unknown")
                link = item.get("link") or item.get("url", "")

                # 名称带链接
                if link:
                    name_str = f"[{name}]({link})"
                else:
                    name_str = name

                lines.append(f"{i}. **{name_str}** - 出现 {count} 次")

                # 描述
                desc = _get_description(item, desc_field)
                if desc:
                    lines.append(f"   - 描述: {desc}")

                lines.append(f"   - 首次发现: {first_seen}")
                lines.append(f"   - 最近出现: {last_seen}")

                # 额外信息
                extra = _get_extra_info(source_key, item)
                if extra:
                    lines.append(f"   - {extra}")

                lines.append("")
        else:
            lines.append("*本周无重复出现的产品*")
            lines.append("")

    if not has_any_repeated:
        lines.append("*本周所有数据源均无重复出现的产品*")
        lines.append("")

    lines.append("---")
    lines.append("")

    return lines


def _generate_new_discoveries_section(insights):
    """生成本周新发现部分"""
    lines = [
        "## 本周新发现",
        "",
        "*只出现一次但值得关注的产品（最近5个）：*",
        "",
    ]

    source_config = [
        ("product_hunt", "Product Hunt", "tagline"),
        ("ai_tools", "AI 工具", "description"),
        ("chrome_extensions", "Chrome 扩展", "description"),
        ("github_trending", "GitHub 项目", "description"),
        ("hacker_news", "Hacker News", None),
    ]

    for source_key, section_name, desc_field in source_config:
        source_data = insights.get(source_key, {})
        new_items = source_data.get("new", [])

        lines.append(f"### {section_name}")
        lines.append("")

        if new_items:
            for i, item_data in enumerate(new_items[:5], 1):
                item = item_data["item"]
                date = _format_date(item_data["last_seen"])

                name = item.get("name") or item.get("title", "Unknown")
                link = item.get("link") or item.get("url", "")

                # 名称带链接
                if link:
                    name_str = f"[{name}]({link})"
                else:
                    name_str = name

                # 描述
                desc = _get_description(item, desc_field)
                if desc:
                    lines.append(f"{i}. **{name_str}** ({date}) - {desc}")
                else:
                    lines.append(f"{i}. **{name_str}** ({date})")

            lines.append("")
        else:
            lines.append("*本周无新发现*")
            lines.append("")

    lines.append("---")
    lines.append("")

    return lines


def _generate_statistics_section(insights):
    """生成分类统计部分"""
    lines = [
        "## 分类统计",
        "",
    ]

    source_names = {
        "product_hunt": "Product Hunt",
        "ai_tools": "AI 工具",
        "chrome_extensions": "Chrome 扩展",
        "github_trending": "GitHub 项目",
        "hacker_news": "Hacker News",
    }

    for source_key, name in source_names.items():
        source_data = insights.get(source_key, {})
        total = source_data.get("total", 0)
        unique = source_data.get("unique", 0)
        repeated_count = len(source_data.get("repeated", []))

        lines.append(f"### {name}")
        lines.append(f"- 总数: {total} 个")
        lines.append(f"- 去重后: {unique} 个")
        lines.append(f"- 重复出现: {repeated_count} 个")
        lines.append("")

    return lines


def _format_date(date_str):
    """格式化日期为更友好的格式"""
    if not date_str:
        return "未知"
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt.month}月{dt.day}日"
    except ValueError:
        return date_str


def _get_description(item, desc_field):
    """获取并截断描述"""
    desc = ""
    if desc_field and desc_field in item:
        desc = item[desc_field]
    elif "tagline" in item:
        desc = item["tagline"]
    elif "description" in item:
        desc = item["description"]

    if desc:
        # 截断到100字符
        desc = str(desc).strip()
        if len(desc) > 100:
            desc = desc[:97] + "..."

    return desc


def _get_extra_info(source_key, item):
    """获取数据源特定的额外信息"""
    if source_key == "chrome_extensions":
        users = item.get("users", "")
        rating = item.get("rating", "")
        if users or rating:
            return f"安装量: {users} | 评分: {rating}"
    elif source_key == "github_trending":
        stars = item.get("today_stars", "")
        if stars:
            return f"热度: {stars}"
    elif source_key == "hacker_news":
        score = item.get("score", 0)
        comments = item.get("comments", 0)
        return f"分数: {score} | 评论: {comments}"
    return ""
