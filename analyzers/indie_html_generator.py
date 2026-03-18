"""Indie opportunity HTML report generator — dark theme matching docs/index.html"""

import re
from datetime import datetime
from zoneinfo import ZoneInfo

from analyzers.indie_analyzer import (
    filter_unsuitable_products,
    score_product,
    deep_analyze_product,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _e(text):
    """HTML-escape a value."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _parse_deep_dive(md):
    """
    Parse the markdown produced by deep_analyze_product() into a structured dict.

    Returns:
        {
          "name": str,
          "source": str,
          "url": str,
          "description": str,
          "qa": [(question, answer), ...],   # 8 items
          "first_step": str,
        }
    """
    result = {"name": "", "source": "", "url": "", "description": "", "qa": [], "first_step": ""}

    # Name from first heading: ## #1 — Name
    m = re.search(r"^## #\d+ — (.+)$", md, re.MULTILINE)
    if m:
        result["name"] = m.group(1).strip()

    # Source
    m = re.search(r"Source: `([^`]+)`", md)
    if m:
        result["source"] = m.group(1).strip()

    # URL
    m = re.search(r"\[([^\]]+)\]\(([^)]+)\)", md)
    if m and m.group(2).startswith("http"):
        result["url"] = m.group(2)

    # Description
    m = re.search(r"\*\*Description:\*\* (.+)", md)
    if m:
        result["description"] = m.group(1).strip()

    # Q&A sections: ### N. Question\nanswer
    qa_pattern = re.findall(
        r"### \d+\. (.+?)\n([\s\S]+?)(?=### \d+\.|---|\Z)",
        md,
    )
    for question, answer in qa_pattern:
        # Clean up the answer: strip leading/trailing whitespace, collapse blank lines
        answer = answer.strip()
        # Remove blockquote markers (> ) for inline display
        answer = re.sub(r"^\s*>\s?", "", answer, flags=re.MULTILINE)
        result["qa"].append((question.strip(), answer.strip()))

    # First step
    m = re.search(r"💡 \*\*First Step:\*\* (.+)", md)
    if m:
        result["first_step"] = m.group(1).strip()

    return result


def _score_bar(value, max_val=5):
    """Render a small score bar as inline HTML."""
    pct = int(value / max_val * 100)
    return (
        f'<div class="score-bar-wrap" title="{value}/{max_val}">'
        f'<div class="score-bar" style="width:{pct}%"></div>'
        f'<span class="score-num">{value}</span>'
        f"</div>"
    )


def _product_url(product):
    """Return the best URL for a product, constructing GitHub URLs from repo name."""
    source = product.get("_source", "")
    if source == "github":
        name = product.get("name", "")
        return f"https://github.com/{name}" if name else ""
    return (
        product.get("link")
        or product.get("url")
        or product.get("website")
        or ""
    )


def _link_label(source):
    """Return appropriate button label for a given source."""
    if source == "github":
        return "View on GitHub →"
    if source == "hackernews":
        return "View on HN →"
    return "Visit Product →"


def _score_color(total):
    """Return a CSS class name based on total score."""
    if total >= 16:
        return "score-high"
    if total >= 12:
        return "score-mid"
    return "score-low"


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

_CSS = """
    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #0f1117;
        color: #e2e8f0;
        line-height: 1.6;
    }

    /* ── Header ── */
    .header {
        background: linear-gradient(135deg, #1a1f2e 0%, #16213e 100%);
        border-bottom: 1px solid #2d3748;
        padding: 32px 24px;
        text-align: center;
    }
    .header h1 { font-size: 3rem; font-weight: 700; color: #fff; letter-spacing: -0.5px; }
    .header h1 span { color: #60a5fa; }
    .header .date { margin-top: 8px; font-size: 14px; color: #718096; }

    .nav-links {
        display: flex;
        justify-content: center;
        gap: 16px;
        margin-top: 16px;
        flex-wrap: wrap;
    }
    .nav-link {
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
    .nav-link:hover { background: #2d5a8e; }

    /* ── Stats bar ── */
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 32px;
        flex-wrap: wrap;
        padding: 20px 16px;
        background: #13171f;
        border-bottom: 1px solid #2d3748;
    }
    .stat { text-align: center; }
    .stat-num { font-size: 28px; font-weight: 700; color: #60a5fa; }
    .stat-label { font-size: 12px; color: #718096; margin-top: 2px; }

    /* ── Container ── */
    .container { max-width: 1100px; margin: 0 auto; padding: 32px 16px 64px; }

    /* ── Section headers ── */
    .section { margin-bottom: 48px; }
    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid #2d3748;
    }
    .section-icon {
        width: 32px; height: 32px; border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px; flex-shrink: 0;
    }
    .section-title { font-size: 18px; font-weight: 600; color: #f7fafc; }
    .section-count {
        margin-left: auto;
        font-size: 12px; color: #718096;
        background: #2d3748;
        padding: 2px 10px; border-radius: 999px;
    }

    /* ── Collapsible (filtered) ── */
    details summary {
        cursor: pointer;
        padding: 10px 14px;
        background: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 8px;
        font-size: 14px;
        color: #a0aec0;
        list-style: none;
        user-select: none;
    }
    details summary::-webkit-details-marker { display: none; }
    details summary::before { content: "▶  "; font-size: 10px; }
    details[open] summary::before { content: "▼  "; }
    details[open] summary { border-radius: 8px 8px 0 0; border-bottom-color: transparent; }
    .details-body {
        border: 1px solid #2d3748;
        border-top: none;
        border-radius: 0 0 8px 8px;
        overflow: hidden;
    }

    /* ── Tables ── */
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th {
        background: #1e2535;
        color: #a0aec0;
        font-weight: 600;
        text-align: left;
        padding: 10px 14px;
        white-space: nowrap;
    }
    th.sortable { cursor: pointer; user-select: none; }
    th.sortable:hover { color: #60a5fa; }
    th.sort-asc::after  { content: " ↑"; color: #60a5fa; }
    th.sort-desc::after { content: " ↓"; color: #60a5fa; }
    td { padding: 10px 14px; border-top: 1px solid #1e2535; color: #e2e8f0; }
    tr:hover td { background: #1a1f2e; }
    .source-tag {
        display: inline-block;
        font-size: 11px; padding: 2px 8px;
        border-radius: 999px;
        background: #2d3748; color: #a0aec0;
    }

    /* ── Score bars ── */
    .score-bar-wrap {
        display: flex; align-items: center; gap: 6px; min-width: 80px;
    }
    .score-bar {
        height: 6px; border-radius: 3px;
        background: #60a5fa; flex-shrink: 0;
    }
    .score-num { font-size: 12px; color: #a0aec0; }
    .score-high { color: #86efac; font-weight: 700; }
    .score-mid  { color: #60a5fa; font-weight: 700; }
    .score-low  { color: #718096; }

    /* ── Top 5 cards ── */
    .top-cards { display: flex; flex-direction: column; gap: 20px; }

    .top-card {
        background: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 12px;
        overflow: hidden;
    }

    .top-card-header {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        padding: 20px;
    }

    .rank-badge {
        flex-shrink: 0;
        width: 40px; height: 40px;
        border-radius: 10px;
        background: #1e3a5f;
        color: #60a5fa;
        font-size: 16px; font-weight: 700;
        display: flex; align-items: center; justify-content: center;
    }

    .top-card-info { flex: 1; min-width: 0; }
    .top-card-name { font-size: 17px; font-weight: 700; color: #f7fafc; }
    .top-card-desc { font-size: 13px; color: #a0aec0; margin-top: 4px; }
    .top-card-meta { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }

    .badge {
        font-size: 11px; padding: 3px 8px;
        border-radius: 6px; font-weight: 500;
    }
    .badge-blue   { background: #1e3a5f; color: #93c5fd; }
    .badge-green  { background: #14532d; color: #86efac; }
    .badge-orange { background: #431407; color: #fb923c; }
    .badge-gray   { background: #2d3748; color: #a0aec0; }

    .top-card-score {
        flex-shrink: 0;
        text-align: center;
        padding: 4px 12px;
        border-radius: 8px;
        background: #0f1117;
    }
    .top-card-score .big { font-size: 22px; font-weight: 700; }
    .top-card-score .label { font-size: 10px; color: #718096; }

    /* ── Expandable Q&A ── */
    .qa-toggle {
        width: 100%;
        background: #13171f;
        border: none; border-top: 1px solid #2d3748;
        padding: 10px 20px;
        color: #718096;
        font-size: 13px;
        text-align: left;
        cursor: pointer;
        display: flex; align-items: center; gap: 6px;
        transition: background 0.2s, color 0.2s;
    }
    .qa-toggle:hover { background: #1a1f2e; color: #a0aec0; }
    .qa-toggle .arrow { font-size: 10px; transition: transform 0.2s; }
    .qa-toggle.open .arrow { transform: rotate(90deg); }
    .qa-toggle.open { color: #60a5fa; }

    .qa-body {
        display: none;
        padding: 0 20px 20px;
        border-top: 1px solid #2d3748;
    }
    .qa-body.open { display: block; }

    .qa-item { margin-top: 18px; }
    .qa-q {
        font-size: 12px; font-weight: 700;
        color: #60a5fa;
        text-transform: uppercase; letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .qa-a {
        font-size: 13px; color: #cbd5e0;
        white-space: pre-wrap;
    }
    .qa-quote {
        margin-top: 6px;
        padding: 8px 12px;
        border-left: 3px solid #2d5a8e;
        background: #13171f;
        border-radius: 0 6px 6px 0;
        font-size: 12px; color: #a0aec0; font-style: italic;
    }
    .first-step {
        margin-top: 18px;
        padding: 12px 16px;
        background: #162032;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
        font-size: 13px; color: #93c5fd;
    }
    .first-step strong { color: #60a5fa; }

    .card-link {
        display: inline-block;
        padding: 6px 16px;
        background: #1e3a5f; color: #60a5fa;
        text-decoration: none; border-radius: 8px;
        font-size: 13px; font-weight: 500;
        transition: background 0.2s;
    }
    .card-link:hover { background: #2d5a8e; color: #93c5fd; }

    @media (max-width: 600px) {
        .header h1 { font-size: 22px; }
        .top-card-header { flex-wrap: wrap; }
        th, td { padding: 8px 10px; }
    }
"""

# ---------------------------------------------------------------------------
# JS for sortable table + Q&A toggles
# ---------------------------------------------------------------------------

_JS = """
    // Sortable table
    document.querySelectorAll('th.sortable').forEach(th => {
        th.addEventListener('click', () => {
            const table = th.closest('table');
            const idx = [...th.parentNode.children].indexOf(th);
            const asc = th.classList.contains('sort-asc');
            table.querySelectorAll('th').forEach(t => t.classList.remove('sort-asc','sort-desc'));
            th.classList.add(asc ? 'sort-desc' : 'sort-asc');
            const tbody = table.querySelector('tbody');
            const rows = [...tbody.querySelectorAll('tr')];
            rows.sort((a, b) => {
                const av = a.children[idx].dataset.val ?? a.children[idx].textContent.trim();
                const bv = b.children[idx].dataset.val ?? b.children[idx].textContent.trim();
                const an = parseFloat(av), bn = parseFloat(bv);
                if (!isNaN(an) && !isNaN(bn)) return asc ? bn - an : an - bn;
                return asc ? bv.localeCompare(av) : av.localeCompare(bv);
            });
            rows.forEach(r => tbody.appendChild(r));
        });
    });

    // Q&A toggles
    document.querySelectorAll('.qa-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const body = btn.nextElementSibling;
            const open = body.classList.toggle('open');
            btn.classList.toggle('open', open);
            btn.querySelector('.qa-label').textContent = open ? 'Hide analysis' : 'Show 8-question analysis';
        });
    });
"""


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate_indie_html(indie_report_markdown, product_data):
    """
    Generate a dark-theme HTML page for the indie opportunity report.

    Args:
        indie_report_markdown: str — the markdown from generate_indie_report()
                                     (used only for reference; HTML is built from data)
        product_data: dict with keys matching generate_indie_report() parameters:
            product_hunt, toolify, ai_tools, chrome_extensions, github, hackernews

    Returns:
        str: Complete HTML document
    """
    pst = ZoneInfo("America/Los_Angeles")
    now = datetime.now(pst)
    tz_abbr = now.strftime("%Z")
    date_str = now.strftime(f"%B %d, %Y · %H:%M {tz_abbr}")

    # ── Re-run analysis (same logic as generate_indie_report) ─────────────
    toolify_raw = product_data.get("toolify", [])
    if isinstance(toolify_raw, dict):
        toolify_list = toolify_raw.get("new", []) + toolify_raw.get("trending", [])
    else:
        toolify_list = toolify_raw or []

    all_products = {
        "product_hunt":     product_data.get("product_hunt", []),
        "toolify":          toolify_list,
        "ai_tools":         product_data.get("ai_tools", []),
        "chrome_extensions": product_data.get("chrome_extensions", []),
        "github":           product_data.get("github", []),
        "hackernews":       product_data.get("hackernews", []),
    }

    suitable, filtered_out = filter_unsuitable_products(all_products)
    for p in suitable:
        p["_scores"] = score_product(p)
    suitable.sort(key=lambda p: p["_scores"]["total_score"], reverse=True)
    top5 = suitable[:5]

    total_input = sum(len(v) for v in all_products.values())

    # ── Section 1: Filtered Out (collapsible) ──────────────────────────────
    if filtered_out:
        rows = "".join(
            f"""<tr>
                <td>{_e(p.get("name") or p.get("title") or "Unknown")}</td>
                <td><span class="source-tag">{_e(p.get("_source","?"))}</span></td>
                <td style="color:#718096;font-size:12px">{_e(p.get("filter_reason",""))}</td>
            </tr>"""
            for p in filtered_out
        )
        filtered_html = f"""
        <details>
            <summary>{len(filtered_out)} products removed from consideration</summary>
            <div class="details-body">
                <table>
                    <thead><tr>
                        <th>Product</th><th>Source</th><th>Reason</th>
                    </tr></thead>
                    <tbody>{rows}</tbody>
                </table>
            </div>
        </details>"""
    else:
        filtered_html = '<p style="color:#718096;font-size:13px">No products were filtered out.</p>'

    # ── Section 2: Quick Score table (sortable) ────────────────────────────
    score_rows = "".join(
        f"""<tr>
            <td data-val="{i}">{i}</td>
            <td>{
                (lambda u, n: f'<a href="{_e(u)}" target="_blank" rel="noopener" style="color:#60a5fa;text-decoration:none">{_e(n)}</a>'
                 if u else _e(n))(
                    _product_url(p),
                    p.get("name") or p.get("title") or "Unknown"
                )
            }</td>
            <td><span class="source-tag">{_e(p.get("_source","?"))}</span></td>
            <td data-val="{p['_scores']['tech_difficulty']}">{_score_bar(p['_scores']['tech_difficulty'])}</td>
            <td data-val="{p['_scores']['user_acquisition']}">{_score_bar(p['_scores']['user_acquisition'])}</td>
            <td data-val="{p['_scores']['revenue_potential']}">{_score_bar(p['_scores']['revenue_potential'])}</td>
            <td data-val="{p['_scores']['indie_friendly']}">{_score_bar(p['_scores']['indie_friendly'])}</td>
            <td data-val="{p['_scores']['total_score']}">
                <span class="{_score_color(p['_scores']['total_score'])}">{p['_scores']['total_score']}</span>
            </td>
        </tr>"""
        for i, p in enumerate(suitable, 1)
    )

    score_html = f"""
    <table>
        <thead><tr>
            <th class="sortable">#</th>
            <th class="sortable">Product</th>
            <th class="sortable">Source</th>
            <th class="sortable">Tech Difficulty</th>
            <th class="sortable">User Acquisition</th>
            <th class="sortable">Revenue Potential</th>
            <th class="sortable">Indie Friendly</th>
            <th class="sortable sort-desc">Total ↓</th>
        </tr></thead>
        <tbody>{score_rows}</tbody>
    </table>"""

    # ── Section 3: Top 5 deep-dive cards ──────────────────────────────────
    card_htmls = []
    for rank, product in enumerate(top5, 1):
        md = deep_analyze_product(product, rank)
        parsed = _parse_deep_dive(md)
        s = product["_scores"]
        total = s["total_score"]
        score_cls = _score_color(total)

        name = parsed["name"] or product.get("name") or product.get("title") or "Unknown"
        desc = parsed["description"] or product.get("description") or product.get("tagline") or ""
        source = parsed["source"] or product.get("_source", "")
        url = _product_url(product) or parsed["url"]

        if url:
            link_html = (
                f'<a class="card-link" href="{_e(url)}" target="_blank" rel="noopener">'
                f'{_link_label(source)}'
                f'</a>'
            )
        else:
            link_html = '<span style="font-size:12px;color:#4a5568">URL not available</span>'

        # Score badges for header
        badges_html = (
            f'<span class="badge badge-blue">Tech {s["tech_difficulty"]}/5</span>'
            f'<span class="badge badge-green">Acquisition {s["user_acquisition"]}/5</span>'
            f'<span class="badge badge-orange">Revenue {s["revenue_potential"]}/5</span>'
            f'<span class="badge badge-gray">Indie {s["indie_friendly"]}/5</span>'
        )

        # Q&A items
        qa_items_html = ""
        for q, a in parsed["qa"]:
            # Split out any blockquote line
            lines = a.split("\n")
            main_lines, quote_lines = [], []
            for ln in lines:
                if ln.startswith('"') or ln.startswith("'") or "What the product says" in ln:
                    quote_lines.append(ln.strip('"').strip("'").strip())
                else:
                    main_lines.append(ln)
            main_text = _e("\n".join(main_lines).strip())
            quote_html = ""
            if quote_lines:
                quote_text = " ".join(quote_lines).strip('"').strip()
                quote_html = f'<div class="qa-quote">{_e(quote_text)}</div>'
            qa_items_html += f"""
            <div class="qa-item">
                <div class="qa-q">{_e(q)}</div>
                <div class="qa-a">{main_text}</div>
                {quote_html}
            </div>"""

        first_step_html = ""
        if parsed["first_step"]:
            first_step_html = (
                f'<div class="first-step">'
                f'<strong>💡 First Step:</strong> {_e(parsed["first_step"])}'
                f"</div>"
            )

        card_htmls.append(f"""
        <div class="top-card">
            <div class="top-card-header">
                <div class="rank-badge">#{rank}</div>
                <div class="top-card-info">
                    <div class="top-card-name">{_e(name)}</div>
                    <div class="top-card-desc">{_e(desc)}</div>
                    <div class="top-card-meta">
                        <span class="source-tag">{_e(source)}</span>
                        {badges_html}
                        {link_html}
                    </div>
                </div>
                <div class="top-card-score">
                    <div class="big {score_cls}">{total}</div>
                    <div class="label">/ 20</div>
                </div>
            </div>
            <button class="qa-toggle">
                <span class="arrow">▶</span>
                <span class="qa-label">Show 8-question analysis</span>
            </button>
            <div class="qa-body">
                {qa_items_html}
                {first_step_html}
            </div>
        </div>""")

    top5_html = f'<div class="top-cards">{"".join(card_htmls)}</div>'

    # ── Assemble page ──────────────────────────────────────────────────────
    def _section(icon, bg, title, content, count_label):
        return f"""
    <div class="section">
        <div class="section-header">
            <div class="section-icon" style="background:{bg}">{icon}</div>
            <span class="section-title">{title}</span>
            <span class="section-count">{count_label}</span>
        </div>
        {content}
    </div>"""

    sections_html = (
        _section("🚫", "#2d1515", "Filtered Out", filtered_html,
                 f"{len(filtered_out)} removed")
        + _section("⭐", "#1a1a0a", "Quick Score — All Suitable Products", score_html,
                   f"{len(suitable)} products")
        + _section("🎯", "#0a1e35", "Top 5 Deep Dive", top5_html, "top 5")
    )

    stats_html = f"""
    <div class="stats-bar">
        <div class="stat">
            <div class="stat-num">{total_input}</div>
            <div class="stat-label">Products Analysed</div>
        </div>
        <div class="stat">
            <div class="stat-num">{len(filtered_out)}</div>
            <div class="stat-label">Filtered Out</div>
        </div>
        <div class="stat">
            <div class="stat-num">{len(suitable)}</div>
            <div class="stat-label">Scored</div>
        </div>
        <div class="stat">
            <div class="stat-num">5</div>
            <div class="stat-label">Deep Dives</div>
        </div>
    </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indie Opportunities — {now.strftime("%Y-%m-%d")}</title>
    <style>{_CSS}</style>
</head>
<body>
    <div class="header">
        <h1>Indie <span>Opportunities</span></h1>
        <div class="date">{date_str}</div>
        <div class="nav-links">
            <a class="nav-link" href="index.html">← View All Products</a>
        </div>
    </div>
    {stats_html}
    <div class="container">
        {sections_html}
    </div>
    <script>{_JS}</script>
</body>
</html>"""
