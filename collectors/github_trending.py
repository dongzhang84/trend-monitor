"""GitHub Trending 采集器"""

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


def fetch_trending_repos(limit=5):
    """抓取GitHub trending页面并提取项目信息"""
    url = "https://github.com/trending"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    repos = []

    # 查找所有repo项目
    articles = soup.select("article.Box-row")[:limit]

    for article in articles:
        # 仓库名称
        name_tag = article.select_one("h2 a")
        if not name_tag:
            continue
        repo_name = name_tag.get("href", "").strip("/")

        # 项目描述
        desc_tag = article.select_one("p")
        description = desc_tag.get_text(strip=True) if desc_tag else "无描述"

        # 今日stars
        stars_tag = article.select_one("span.d-inline-block.float-sm-right")
        today_stars = stars_tag.get_text(strip=True) if stars_tag else "N/A"

        repos.append({
            "name": repo_name,
            "description": description,
            "today_stars": today_stars,
        })

    return repos
