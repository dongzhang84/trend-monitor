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
    """获取 There's An AI For That 网站的AI工具列表"""
    url = "https://theresanaiforthat.com/"

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    tools = []

    # 查找工具卡片
    tool_cards = soup.select(".li")[:limit * 3]  # 获取更多以防有些不完整

    for card in tool_cards:
        if len(tools) >= limit:
            break

        # 查找所有 a 标签
        links = card.find_all("a")
        if not links:
            continue

        # 第一个 a 标签通常包含工具名称和链接
        first_link = links[0]
        name = first_link.get_text(strip=True)
        href = first_link.get("href", "")

        # 只处理 /ai/ 开头的链接（真正的工具）
        if not href.startswith("/ai/"):
            continue

        link = "https://theresanaiforthat.com" + href

        # 获取整个卡片的文本，从中提取描述
        # 描述通常紧跟在工具名后面
        full_text = card.get_text(separator="|", strip=True)
        parts = full_text.split("|")

        # 第一部分是名称，第二部分通常是描述
        description = parts[1] if len(parts) > 1 else "无描述"

        # 查找分类（链接到 /task/ 的标签）
        category = "AI工具"
        for a_tag in links:
            task_href = a_tag.get("href", "")
            if task_href.startswith("/task/"):
                category = a_tag.get_text(strip=True)
                break

        if name and len(name) > 1:
            tools.append({
                "name": name,
                "description": description,
                "category": category,
                "link": link,
            })

    return tools
