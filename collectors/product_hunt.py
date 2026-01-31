"""Product Hunt 采集器"""

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}


def fetch_product_hunt_posts(limit=5):
    """通过RSS feed获取Product Hunt产品信息"""
    url = "https://www.producthunt.com/feed"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return []

    soup = BeautifulSoup(response.text, "xml")
    products = []

    entries = soup.find_all("entry")[:limit]

    for entry in entries:
        # 产品名称
        title_tag = entry.find("title")
        name = title_tag.get_text(strip=True) if title_tag else "未知产品"

        # 产品描述 (从content中提取)
        content_tag = entry.find("content")
        tagline = "无描述"
        if content_tag:
            content_soup = BeautifulSoup(content_tag.get_text(), "html.parser")
            # 描述通常在第一个p标签
            p_tag = content_soup.find("p")
            if p_tag:
                tagline = p_tag.get_text(strip=True)

        # 产品链接
        link_tag = entry.find("link")
        link = link_tag.get("href", "N/A") if link_tag else "N/A"

        products.append({
            "name": name,
            "tagline": tagline,
            "link": link,
        })

    return products
