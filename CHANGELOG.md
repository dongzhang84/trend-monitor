# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-03-17

### Added
- Toolify.ai data source with two sections: latest tools (`/new`) and trending tools (`/Best-trending-AI-Tools`)
- Trending tools include monthly visit count and growth rate (e.g. `1054%`)
- Toolify section in daily report (最新上线 + Trending 榜单)
- Toolify integrated into weekly report: overview, repeated items, new discoveries, statistics
- Playwright-based scraper to bypass Cloudflare protection on Toolify.ai

### Changed
- Data source count increased from 5 to 6
- Daily data JSON now includes `toolify` field (combined new + trending, 10 items)
- Report section order: Product Hunt → Toolify → TAAFT → Chrome Extensions → GitHub → Hacker News
- Weekly report overview and statistics updated to include Toolify Trending

### Technical
- Added `collectors/toolify.py` with `fetch_new_tools()`, `fetch_trending_tools()`, `fetch_toolify_tools()`
- Added `playwright>=1.40.0` to `requirements.txt`
- Both GitHub Actions workflows now install Chromium via `playwright install chromium --with-deps`
- Toolify returns `{'new': [...], 'trending': [...]}` dict; stored as merged flat list for weekly analysis

## [1.2.2] - 2026-02-04

### Fixed
- Chrome Extension rating display issue (fixed rating extraction logic)
- There's An AI For That data source changed to `/new/` page (latest tools instead of stale trending)
- Filter out B2B tools, focus on personal-use tools
- Daily report send time adjusted from 7:30 AM to 7:00 AM PST

## [1.2.1] - 2026-02-02

### Fixed
- Chrome Extension 评分获取失败（选择器从 `ratingValue` 改为 `aria-label`）
- There's An AI For That 改为抓取 `/popular/` 页面而非首页，提升数据质量

## [1.2.0] - 2026-01-31

### Added
- Weekly report automation - comprehensive trend analysis every Sunday
- Daily data storage to JSON files for historical tracking
- Weekly analyzer with frequency analysis and keyword extraction
- Repeated items detection (products appearing multiple times)
- Top keywords analysis across all data sources
- GitHub Actions weekly workflow (every Sunday 22:00 PST)

### Technical
- Added `storage/` module for daily data persistence
- Added `analyzers/` module for weekly data analysis
- Added `reporters/weekly_report_generator.py` for weekly report generation
- Added `weekly_report.py` entry script for weekly automation
- Added `.github/workflows/weekly-report.yml`
- Weekly reports saved to `reports/weekly/weekly-YYYY-MM-DD.md`
- Data retention: 4 weeks (28 days)

## [1.1.0] - 2026-01-31

### Added
- There's An AI For That data source for AI tool discovery
- Chrome Extensions dynamic scraper with random keyword search
- Focus shift: from developer tools to business opportunity discovery

### Changed
- Data source priority: Product Hunt moved to #1 position
- Report structure: Product Hunt → AI Tools → Chrome Extensions → GitHub → Hacker News
- Chrome Extensions: dynamic search instead of hardcoded list

### Technical
- Added `collectors/theresanaiforthat.py`
- Added `collectors/chrome_extensions.py` (refactored from hardcoded IDs to dynamic scraping)
- Updated report generator to support 5 data sources

## [1.0.0] - 2026-01-30

### Added
- GitHub Trending monitoring (top repositories by daily stars)
- Product Hunt monitoring (daily hot products via RSS)
- Hacker News monitoring (top stories via official API)
- Markdown report generation with structured sections
- Email delivery via SMTP (Gmail compatible)
- GitHub Actions automation (daily at 7:30 AM PST)
- PST timezone support for report timestamps
- Complete English documentation (README.md)
- Environment-based configuration (.env support)
