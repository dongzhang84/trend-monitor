"""HTML report generator - dark theme, card-based layout"""

from datetime import datetime
from zoneinfo import ZoneInfo


def generate_html_report(
    product_hunt_data,
    toolify_data,
    ai_tools_data,
    chrome_extensions_data,
    github_trending_data,
    hackernews_data,
):
    """
    Generate a responsive dark-theme HTML report from all data sources.

    Args:
        product_hunt_data: list of {name, tagline, link}
        toolify_data: dict {'new': [{name, description, category, link}],
                            'trending': [{name, description, monthly_visit, growth_rate, link}]}
        ai_tools_data: list of {name, description, category, link}
        chrome_extensions_data: list of {name, description, users, rating, link}
        github_trending_data: list of {name, description, today_stars}
        hackernews_data: list of {title, author, score, comments, url}

    Returns:
        str: Complete HTML document
    """
    pst = ZoneInfo("America/Los_Angeles")
    now = datetime.now(pst)
    tz_abbr = now.strftime("%Z")
    date_str = now.strftime(f"%B %d, %Y · %H:%M {tz_abbr}")

    toolify_new = toolify_data.get("new", []) if isinstance(toolify_data, dict) else []
    toolify_trending = toolify_data.get("trending", []) if isinstance(toolify_data, dict) else []

    css = """
        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f1117;
            color: #e2e8f0;
            line-height: 1.6;
        }

        .header {
            background: linear-gradient(135deg, #1a1f2e 0%, #16213e 100%);
            border-bottom: 1px solid #2d3748;
            padding: 32px 24px;
            text-align: center;
        }

        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            color: #fff;
            letter-spacing: -0.5px;
        }

        .header h1 span { color: #60a5fa; }

        .header .date {
            margin-top: 8px;
            font-size: 14px;
            color: #718096;
        }

        .header-nav {
            display: flex;
            justify-content: center;
            margin-top: 12px;
        }

        .header-nav a {
            display: inline-block;
            padding: 6px 18px;
            background: #1e3a5f;
            color: #60a5fa;
            text-decoration: none;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
            transition: background 0.2s;
        }

        .header-nav a:hover { background: #2d5a8e; }

        .source-pills {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 16px;
        }

        .pill {
            background: #2d3748;
            color: #a0aec0;
            font-size: 12px;
            padding: 4px 12px;
            border-radius: 999px;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 32px 16px 64px;
        }

        .section {
            margin-bottom: 48px;
        }

        .section-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid #2d3748;
        }

        .section-icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
        }

        .section-title {
            font-size: 18px;
            font-weight: 600;
            color: #f7fafc;
        }

        .section-count {
            margin-left: auto;
            font-size: 12px;
            color: #718096;
            background: #2d3748;
            padding: 2px 10px;
            border-radius: 999px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 16px;
        }

        .card {
            background: #1a1f2e;
            border: 1px solid #2d3748;
            border-radius: 12px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            transition: border-color 0.2s;
        }

        .card:hover { border-color: #4a5568; }

        .card-rank {
            font-size: 11px;
            font-weight: 600;
            color: #60a5fa;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .card-name {
            font-size: 15px;
            font-weight: 600;
            color: #f7fafc;
        }

        .card-desc {
            font-size: 13px;
            color: #a0aec0;
            flex: 1;
        }

        .card-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .badge {
            font-size: 11px;
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 500;
        }

        .badge-purple { background: #1e3a5f; color: #60a5fa; }
        .badge-green  { background: #14532d; color: #86efac; }
        .badge-blue   { background: #1e3a5f; color: #93c5fd; }
        .badge-orange { background: #431407; color: #fb923c; }
        .badge-gray   { background: #2d3748; color: #a0aec0; }

        .card-link {
            display: inline-block;
            margin-top: 4px;
            padding: 7px 16px;
            background: #1e3a5f;
            color: #60a5fa;
            text-decoration: none;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
            text-align: center;
            transition: background 0.2s, color 0.2s;
        }

        .card-link:hover { background: #2d5a8e; color: #93c5fd; }

        .subsection-label {
            font-size: 13px;
            font-weight: 600;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin: 24px 0 12px;
        }

        .subsection-label:first-child { margin-top: 0; }

        @media (max-width: 600px) {
            .cards { grid-template-columns: 1fr; }
            .header h1 { font-size: 22px; }
        }
    """

    def e(text):
        """HTML-escape a string."""
        return (
            str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def card(rank, name, desc, link, badges=None):
        badges_html = ""
        if badges:
            badges_html = '<div class="card-meta">'
            for text, style in badges:
                badges_html += f'<span class="badge badge-{style}">{e(text)}</span>'
            badges_html += "</div>"
        return f"""
        <div class="card">
            <div class="card-rank">#{rank}</div>
            <div class="card-name">{e(name)}</div>
            <div class="card-desc">{e(desc)}</div>
            {badges_html}
            <a class="card-link" href="{e(link)}" target="_blank" rel="noopener">View →</a>
        </div>"""

    def section(icon, icon_bg, title, content_html, count):
        return f"""
    <div class="section">
        <div class="section-header">
            <div class="section-icon" style="background:{icon_bg}">{icon}</div>
            <span class="section-title">{title}</span>
            <span class="section-count">{count} items</span>
        </div>
        {content_html}
    </div>"""

    # ── Product Hunt ──────────────────────────────────────────────────────────
    ph_cards = "".join(
        card(i, p["name"], p.get("tagline", ""), p["link"])
        for i, p in enumerate(product_hunt_data, 1)
    )
    ph_html = f'<div class="cards">{ph_cards}</div>'

    # ── Toolify ───────────────────────────────────────────────────────────────
    toolify_parts = []
    if toolify_new:
        new_cards = "".join(
            card(i, t["name"], t.get("description", ""), t["link"],
                 badges=[("New", "purple")] + ([("Category: " + t["category"], "gray")] if t.get("category") else []))
            for i, t in enumerate(toolify_new, 1)
        )
        toolify_parts.append('<div class="subsection-label">Latest</div>')
        toolify_parts.append(f'<div class="cards">{new_cards}</div>')
    if toolify_trending:
        tr_cards = "".join(
            card(i, t["name"], t.get("description", ""), t["link"],
                 badges=[
                     ("📈 " + t["monthly_visit"], "blue") if t.get("monthly_visit") else None,
                     ("↑ " + t["growth_rate"], "green") if t.get("growth_rate") else None,
                 ])
            for i, t in enumerate(toolify_trending, 1)
        )
        toolify_parts.append('<div class="subsection-label">Trending</div>')
        toolify_parts.append(f'<div class="cards">{tr_cards}</div>')
    toolify_html = "\n".join(toolify_parts)
    toolify_count = len(toolify_new) + len(toolify_trending)

    # ── There's An AI For That ────────────────────────────────────────────────
    taaft_cards = "".join(
        card(i, t["name"], t.get("description", ""), t["link"],
             badges=[("Category: " + t["category"], "purple")] if t.get("category") else [])
        for i, t in enumerate(ai_tools_data, 1)
    )
    taaft_html = f'<div class="cards">{taaft_cards}</div>'

    # ── Chrome Extensions ─────────────────────────────────────────────────────
    chrome_cards = "".join(
        card(i, x["name"], x.get("description", ""), x["link"],
             badges=[
                 b for b in [
                     ("👥 " + x["users"], "blue") if x.get("users") else None,
                     ("★ " + x["rating"], "orange") if x.get("rating") else None,
                 ] if b
             ])
        for i, x in enumerate(chrome_extensions_data, 1)
    )
    chrome_html = f'<div class="cards">{chrome_cards}</div>'

    # ── GitHub Trending ───────────────────────────────────────────────────────
    gh_cards = "".join(
        card(i, r["name"], r.get("description", ""),
             f"https://github.com/{r['name']}",
             badges=[("⭐ " + r["today_stars"], "orange")] if r.get("today_stars") else [])
        for i, r in enumerate(github_trending_data, 1)
    )
    gh_html = f'<div class="cards">{gh_cards}</div>'

    # ── Hacker News ───────────────────────────────────────────────────────────
    hn_cards = "".join(
        card(i, p["title"], f"by {p.get('author', 'unknown')}",
             p.get("url", "#"),
             badges=[
                 b for b in [
                     ("▲ " + str(p["score"]), "orange") if p.get("score") else None,
                     ("💬 " + str(p["comments"]), "gray") if p.get("comments") else None,
                 ] if b
             ])
        for i, p in enumerate(hackernews_data, 1)
    )
    hn_html = f'<div class="cards">{hn_cards}</div>'

    # ── Assemble page ─────────────────────────────────────────────────────────
    sections_html = (
        section("🚀", "#1a0533", "Product Hunt", ph_html, len(product_hunt_data))
        + section("⚡", "#0a1e35", "Toolify.ai", toolify_html, toolify_count)
        + section("🤖", "#0a1a2e", "There's An AI For That", taaft_html, len(ai_tools_data))
        + section("🧩", "#0a1a0a", "Chrome Extensions", chrome_html, len(chrome_extensions_data))
        + section("📦", "#1a1a0a", "GitHub Trending", gh_html, len(github_trending_data))
        + section("🔥", "#1a0a0a", "Hacker News", hn_html, len(hackernews_data))
    )

    source_pills = "".join(
        f'<span class="pill">{s}</span>'
        for s in ["Product Hunt", "Toolify.ai", "TAAFT", "Chrome Extensions", "GitHub", "Hacker News"]
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI/Tech Daily Trends</title>
    <style>{css}</style>
</head>
<body>
    <div class="header">
        <h1>AI/Tech <span>Daily Trends</span></h1>
        <div class="date">{date_str}</div>
        <div class="header-nav"><a href="indie.html">View Indie Opportunities →</a></div>
        <div class="source-pills">{source_pills}</div>
    </div>
    <div class="container">
        {sections_html}
    </div>
</body>
</html>"""
