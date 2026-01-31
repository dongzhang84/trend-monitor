"""周报数据分析器"""

import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from storage.data_store import load_daily_data, list_available_dates


# 停用词列表
STOP_WORDS = {
    "the", "a", "an", "for", "with", "and", "or", "to", "of", "in", "on", "at",
    "is", "it", "be", "as", "by", "this", "that", "from", "your", "you", "we",
    "our", "all", "any", "can", "has", "have", "will", "more", "most", "new",
    "one", "two", "using", "use", "used", "into", "are", "was", "been", "being",
    "their", "them", "they", "what", "when", "where", "which", "who", "how",
    "just", "like", "make", "get", "also", "its", "about", "than", "then",
    "only", "other", "such", "some", "each", "every", "but", "not", "no",
}

# 数据源名称映射
SOURCE_NAMES = [
    "product_hunt",
    "ai_tools",
    "chrome_extensions",
    "github_trending",
    "hacker_news",
]


def load_weekly_data(days=7):
    """
    加载过去N天的数据

    Args:
        days: 加载最近多少天的数据

    Returns:
        dict: {
            "dates": ["2026-01-31", "2026-01-30", ...],
            "product_hunt": [所有产品列表],
            "ai_tools": [...],
            ...
        }
    """
    pst = ZoneInfo("America/Los_Angeles")
    today = datetime.now(pst)

    result = {
        "dates": [],
        "product_hunt": [],
        "ai_tools": [],
        "chrome_extensions": [],
        "github_trending": [],
        "hacker_news": [],
    }

    for i in range(days):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        data = load_daily_data(date)

        if data:
            result["dates"].append(date)

            # 为每个条目添加日期标记
            for source in SOURCE_NAMES:
                items = data.get(source, [])
                for item in items:
                    item["_date"] = date
                result[source].extend(items)

    return result


def analyze_frequency(items, key="name"):
    """
    分析产品出现频率

    Args:
        items: 产品列表
        key: 用于匹配的字段名

    Returns:
        list: [(item_info, count, first_seen, last_seen), ...]
        按出现次数降序排序
    """
    # 用于统计
    frequency = defaultdict(lambda: {
        "count": 0,
        "first_seen": None,
        "last_seen": None,
        "item": None,
    })

    for item in items:
        name = item.get(key, "").strip().lower()
        if not name:
            continue

        date = item.get("_date", "")

        freq = frequency[name]
        freq["count"] += 1

        # 更新首次和最后出现日期
        if freq["first_seen"] is None or date < freq["first_seen"]:
            freq["first_seen"] = date
        if freq["last_seen"] is None or date > freq["last_seen"]:
            freq["last_seen"] = date

        # 保存最新的完整信息
        freq["item"] = item

    # 转换为列表并排序
    result = []
    for name, info in frequency.items():
        result.append({
            "item": info["item"],
            "count": info["count"],
            "first_seen": info["first_seen"],
            "last_seen": info["last_seen"],
        })

    # 按出现次数降序，然后按最后出现日期降序
    result.sort(key=lambda x: (-x["count"], x["last_seen"] or ""), reverse=False)

    return result


def extract_keywords(items, top_n=10):
    """
    从产品名称和描述中提取关键词

    Args:
        items: 产品列表
        top_n: 返回前N个关键词

    Returns:
        list: [(keyword, count), ...]
    """
    word_count = defaultdict(int)

    # 提取文本字段
    text_fields = ["name", "title", "description", "tagline"]

    for item in items:
        text_parts = []
        for field in text_fields:
            if field in item and item[field]:
                text_parts.append(str(item[field]))

        text = " ".join(text_parts)

        # 提取单词（只保留英文字母）
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text)

        for word in words:
            word_lower = word.lower()
            if word_lower not in STOP_WORDS:
                word_count[word_lower] += 1

    # 排序并返回Top N
    sorted_words = sorted(word_count.items(), key=lambda x: -x[1])
    return sorted_words[:top_n]


def generate_weekly_insights(days=7):
    """
    生成周报分析洞察

    Args:
        days: 分析最近多少天的数据

    Returns:
        dict: 完整的周报分析结果
    """
    # 加载数据
    data = load_weekly_data(days)

    if len(data["dates"]) < 1:
        return {
            "error": "数据不足",
            "message": f"需要至少1天的数据，当前只有{len(data['dates'])}天",
        }

    # 确定时间范围
    dates = sorted(data["dates"])
    period = {
        "start": dates[0],
        "end": dates[-1],
        "days_with_data": len(dates),
    }

    # 分析每个数据源
    insights = {
        "period": period,
        "keywords": [],
    }

    all_items = []  # 用于提取关键词

    for source in SOURCE_NAMES:
        items = data[source]
        all_items.extend(items)

        # 频率分析
        freq_analysis = analyze_frequency(items, key=_get_name_key(source))

        # 分离重复和新出现的
        repeated = [f for f in freq_analysis if f["count"] >= 2][:10]
        new_items = [f for f in freq_analysis if f["count"] == 1]

        # 新项目按日期降序，取最近5个
        new_items.sort(key=lambda x: x["last_seen"] or "", reverse=True)
        new_items = new_items[:5]

        insights[source] = {
            "total": len(items),
            "unique": len(freq_analysis),
            "repeated": repeated,
            "new": new_items,
        }

    # 提取关键词
    insights["keywords"] = extract_keywords(all_items, top_n=15)

    return insights


def _get_name_key(source):
    """根据数据源返回用于匹配的字段名"""
    if source == "hacker_news":
        return "title"
    return "name"
