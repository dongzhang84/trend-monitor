"""There's An AI For That 采集器"""

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}


def fetch_ai_tools(limit=5):
    """获取 There's An AI For That 网站最新上传的AI工具"""
    # /new/ 页面 - 最新上传的工具
    url = "https://theresanaiforthat.com/new/"

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    tools = []

    # 查找工具卡片 - /new/ 页面用 data-name 属性
    tool_cards = soup.select(".li[data-name]")[:limit * 3]

    for card in tool_cards:
        if len(tools) >= limit:
            break

        # 从 data 属性获取信息
        name = card.get("data-name", "")
        category = card.get("data-task", "AI工具")

        # 获取链接
        ai_link = card.select_one("a.ai_link")
        if not ai_link:
            continue
        href = ai_link.get("href", "")
        link = "https://theresanaiforthat.com" + href

        # 获取描述
        desc_el = card.select_one(".short_desc")
        description = desc_el.get_text(strip=True) if desc_el else ""

        # 跳过无效描述
        if len(description) < 10:
            continue

        if name and len(name) > 1:
            tools.append({
                "name": name,
                "description": description,
                "category": category,
                "link": link,
            })

    return tools
