"""Chrome Extensions 采集器 - 动态爬取 Chrome Web Store"""

import re
import random
import time
import requests
from html import unescape


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
}

# 搜索关键词列表 - 每次随机选择一个，保证结果多样性
SEARCH_KEYWORDS = [
    "AI assistant",
    "productivity tools",
    "AI writing",
    "automation",
    "developer tools",
    "AI chat",
    "workflow",
    "new AI",
]


def fetch_chrome_extensions(limit=5):
    """动态获取 Chrome Web Store 热门扩展"""
    # 随机选择搜索关键词
    keyword = random.choice(SEARCH_KEYWORDS)
    search_url = f"https://chromewebstore.google.com/search/{requests.utils.quote(keyword)}"

    try:
        response = requests.get(search_url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            print(f"    搜索页面请求失败: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"    搜索请求错误: {e}")
        return []

    # 从搜索结果提取扩展ID和名称
    detail_pattern = r'/detail/([^/]+)/([a-z]{32})'
    details = re.findall(detail_pattern, response.text)

    if not details:
        print(f"    未找到扩展列表")
        return []

    extensions = []

    # 获取每个扩展的详细信息
    for name_slug, ext_id in details[:limit + 2]:  # 多获取几个以防有些失败
        if len(extensions) >= limit:
            break

        detail_url = f"https://chromewebstore.google.com/detail/{name_slug}/{ext_id}"

        try:
            # 添加小延迟避免请求过快
            time.sleep(0.3)

            detail_resp = requests.get(detail_url, headers=HEADERS, timeout=15)
            if detail_resp.status_code != 200:
                continue

            html = detail_resp.text

            # 提取标题
            title_match = re.search(r"<title>([^<]+)</title>", html)
            name = "Unknown"
            if title_match:
                name = title_match.group(1).replace(" - Chrome Web Store", "").strip()
                name = unescape(name)

            # 提取用户数
            user_match = re.search(r">(\d[\d,]+)\s*users?<", html)
            users = user_match.group(1) + " users" if user_match else "N/A"

            # 提取描述
            desc_match = re.search(r'<meta name="description" content="([^"]+)"', html)
            description = "无描述"
            if desc_match:
                description = unescape(desc_match.group(1))

            # 提取评分 (从 aria-label="4.7 out of 5 stars" 格式)
            rating = "N/A"
            rating_match = re.search(r'aria-label="([0-9.]+) out of 5 stars?"', html)
            if rating_match:
                rating = f"{rating_match.group(1)}/5.0"

            extensions.append({
                "name": name,
                "description": description,
                "users": users,
                "rating": rating,
                "link": detail_url,
            })

        except requests.RequestException:
            continue

    return extensions
