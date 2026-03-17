"""Toolify.ai 采集器 - 最新工具(new) + Trending工具"""

import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def _get_page_html(url, wait_seconds=8):
    """使用 Playwright 绕过 Cloudflare 获取页面 HTML"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
            )
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800},
            )
            page = context.new_page()
            page.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            time.sleep(wait_seconds)  # 等待 Cloudflare 验证完成
            html = page.content()
            browser.close()
            return html
    except PlaywrightTimeoutError as e:
        print(f"    页面加载超时: {e}")
        return ""
    except Exception as e:
        print(f"    Playwright 错误: {e}")
        return ""


def _parse_new_tools(html, limit):
    """解析 /new 页面（卡片结构）"""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    tools = []

    items = [i for i in soup.select(".tool-item") if i.get("data-advertisement_id") == ""]

    for item in items:
        if len(tools) >= limit:
            break

        handle = item.get("data-handle", "")
        if not handle:
            continue

        name_el = item.select_one(".tool-name")
        name = name_el.get_text(strip=True) if name_el else ""
        if not name:
            continue

        desc_el = item.select_one(".tool-desc")
        description = desc_el.get_text(strip=True) if desc_el else ""
        if len(description) < 5:
            continue

        link_el = item.select_one("a[href]")
        href = link_el.get("href", "") if link_el else ""
        if href.startswith("/"):
            link = "https://www.toolify.ai" + href
        else:
            link = f"https://www.toolify.ai/tool/{handle}"

        category = item.get("data-position", "AI工具")

        tools.append({
            "name": name,
            "description": description,
            "category": category,
            "link": link,
        })

    return tools


def _parse_trending(html, limit):
    """解析 /Best-trending-AI-Tools 页面（表格结构）

    列顺序：Ranking | Tools | Monthly Visit | Visit Change | Growth Rate | Description | Categories
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    tools = []

    rows = soup.select("tr.el-table__row")
    for row in rows:
        if len(tools) >= limit:
            break

        tds = row.select("td")
        if len(tds) < 6:
            continue

        link_el = tds[1].select_one("a.go-tool")
        if not link_el:
            continue
        name = link_el.get_text(strip=True)
        if not name:
            continue
        href = link_el.get("href", "")
        link = ("https://www.toolify.ai" + href) if href.startswith("/") else href

        visit_el = tds[2].select_one("span")
        monthly_visit = visit_el.get_text(strip=True) if visit_el else ""

        growth_el = tds[4].select_one("span")
        growth_rate = growth_el.get_text(strip=True) if growth_el else ""

        desc_el = tds[5].select_one("p.tool-desc")
        description = desc_el.get_text(strip=True) if desc_el else ""

        tools.append({
            "name": name,
            "description": description,
            "monthly_visit": monthly_visit,
            "growth_rate": growth_rate,
            "link": link,
        })

    return tools


def fetch_new_tools(limit=5):
    """获取 Toolify.ai 最新上线的 AI 工具"""
    try:
        html = _get_page_html("https://www.toolify.ai/new")
        if not html:
            return []
        return _parse_new_tools(html, limit)
    except Exception as e:
        print(f"获取最新工具失败: {e}")
        return []


def fetch_trending_tools(limit=5):
    """获取 Toolify.ai Trending AI 工具"""
    try:
        html = _get_page_html("https://www.toolify.ai/Best-trending-AI-Tools")
        if not html:
            return []
        return _parse_trending(html, limit)
    except Exception as e:
        print(f"获取 Trending 工具失败: {e}")
        return []


def fetch_toolify_tools():
    """获取 Toolify.ai 数据：new（最新）在前，trending在后"""
    print("  正在获取 Toolify.ai 最新工具(new)...")
    new = fetch_new_tools(5)
    print(f"  获取到 {len(new)} 个最新工具")

    print("  正在获取 Toolify.ai Trending 工具...")
    trending = fetch_trending_tools(5)
    print(f"  获取到 {len(trending)} 个 Trending 工具")

    return {
        "new": new,
        "trending": trending,
    }


if __name__ == "__main__":
    result = fetch_toolify_tools()
    print("\n最新工具:")
    for t in result["new"]:
        print(f"  - {t['name']}: {t['description'][:60]}")
    print("\nTrending 工具:")
    for t in result["trending"]:
        print(f"  - {t['name']} | 月访问: {t['monthly_visit']} | 增长: {t['growth_rate']}")
