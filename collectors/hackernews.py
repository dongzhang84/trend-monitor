"""Hacker News 采集器"""

import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
}

HN_API_BASE = "https://hacker-news.firebaseio.com/v0"


def fetch_hackernews_posts(limit=5):
    """通过官方API获取Hacker News热门文章"""
    try:
        # 获取top stories列表
        response = requests.get(f"{HN_API_BASE}/topstories.json", headers=HEADERS, timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:limit]
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []

    posts = []
    for story_id in story_ids:
        try:
            # 获取单个story详情
            response = requests.get(f"{HN_API_BASE}/item/{story_id}.json", headers=HEADERS, timeout=10)
            response.raise_for_status()
            story = response.json()

            if not story:
                continue

            # 如果没有url，使用HN讨论链接
            url = story.get("url") or f"https://news.ycombinator.com/item?id={story_id}"

            posts.append({
                "title": story.get("title", "无标题"),
                "author": story.get("by", "unknown"),
                "score": story.get("score", 0),
                "comments": story.get("descendants", 0),
                "url": url,
            })
        except requests.RequestException:
            continue

    return posts
