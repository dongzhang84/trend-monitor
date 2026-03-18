# AI/Tech Trend Monitor

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Daily business opportunity discovery tool - monitors AI products and trending tools from 6 sources. Get a curated digest delivered to your inbox every morning **and** browse a live web dashboard updated automatically every day.

## Live Demo

**[View Today's Report →](https://dongzhang84.github.io/trend-monitor/)**

![Dashboard screenshot](images/screenshot_1.png)

The dashboard updates automatically every morning via GitHub Actions. Dark theme, responsive layout, clickable cards for all 6 data sources.

## Features

- **Multi-source Aggregation** - Collects data from 6 sources: Product Hunt, Toolify.ai, There's An AI For That, Chrome Extensions, GitHub, Hacker News
- **Web Dashboard** - Live HTML report at GitHub Pages, dark theme, responsive card layout, auto-updated daily
- **Indie Opportunity Analysis** - Daily report scoring products for solo-builder viability with an 8-question deep-dive per top pick
- **Automated Reports** - Generates Markdown reports and HTML dashboard on every run
- **Weekly Reports** - Automated weekly summaries with trend analysis every Sunday 22:00 PST
- **Email Delivery** - Sends formatted HTML emails directly to your inbox
- **GitHub Actions** - Fully automated daily and weekly execution with auto-deploy to GitHub Pages
- **Zero Cost** - Uses free APIs, GitHub Actions, and GitHub Pages (no paid services required)

## Data Sources

| Source | Data Collected |
|--------|---------------|
| **Product Hunt** | Product name, tagline, product link |
| **Toolify.ai** | Latest tools (name, description, link) + Trending tools (name, description, monthly visits, growth rate, link) |
| **There's An AI For That** | AI tool name, description, category, link |
| **Chrome Extensions** | Extension name, description, users, rating, link |
| **GitHub Trending** | Repository name, description, daily stars |
| **Hacker News** | Title, author, score, comment count, link |

## Installation

### Prerequisites

- Python 3.9 or higher
- A Gmail account (for email delivery)

### Setup

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/trend-monitor.git
cd trend-monitor
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
playwright install chromium --with-deps
```

3. **Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` with your email credentials (see [Configuration](#configuration) below).

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# SMTP Settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Email Credentials
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx
EMAIL_RECEIVER=your-email@gmail.com
```

### Gmail App Password Setup

Gmail requires an "App Password" instead of your regular password. Follow these steps:

1. **Enable 2-Step Verification**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Click on "2-Step Verification"
   - Follow the prompts to enable it

2. **Generate App Password**
   - Go to [App Passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" as the app
   - Select "Other" as the device and name it (e.g., "Trend Monitor")
   - Click "Generate"

3. **Copy the 16-character password**
   - Use this password as `EMAIL_PASSWORD` in your `.env` file
   - Format: `xxxx xxxx xxxx xxxx` (spaces optional)

## Usage

### Local Execution

```bash
# Run with email delivery
python main.py

# Run without email (report only)
python main.py --no-email
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--no-email` | Skip email delivery, only generate report.md |

### Output

The script generates three files on every run:

| File | Description |
|------|-------------|
| `report.md` | Markdown report (local reference) |
| `docs/index.html` | Dark-theme HTML dashboard (published to GitHub Pages) |
| `analysis/daily/{date}-indie.md` | Indie hacker opportunity analysis (auto-committed by CI) |

## GitHub Actions Setup

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/trend-monitor.git
git push -u origin main
```

### 2. Configure Repository Secrets

Go to your repository on GitHub:

1. Navigate to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the following secrets:

| Secret Name | Value |
|-------------|-------|
| `EMAIL_SENDER` | Your Gmail address |
| `EMAIL_PASSWORD` | Your Gmail App Password |
| `EMAIL_RECEIVER` | Recipient email address |
| `SMTP_SERVER` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |

### 3. Enable GitHub Pages

After your first workflow run, enable GitHub Pages to host the HTML dashboard:

1. Go to **Settings** → **Pages**
2. Under **Source**, select **Deploy from a branch**
3. Branch: `main`, folder: `/docs`
4. Click **Save**

Your dashboard will be live at `https://YOUR_USERNAME.github.io/trend-monitor/`

### 4. Schedule

The workflows run automatically:
- **Daily Reports**: 7:00 AM PST (every day) — generates email + HTML dashboard + commits to repo
- **Weekly Reports**: 10:00 PM PST (every Sunday) — generates trend analysis email

To manually trigger a workflow:
1. Go to **Actions** tab
2. Select **Daily Trend Report** or **Weekly Trend Report**
3. Click **Run workflow**

## Weekly Reports

The system automatically generates comprehensive weekly reports every Sunday at 22:00 PST.

### Weekly Report Features

- **Repeated Items**: Products/tools that appeared multiple times during the week
- **New Discoveries**: Unique products that appeared only once
- **Keyword Analysis**: Top 10 trending keywords across all sources
- **Statistics**: Data overview and category breakdown

### Report Structure

Weekly reports include:
- Data overview (total items monitored)
- Hot keywords (top 10)
- Repeated appearances (showing persistence)
- New discoveries (latest finds)
- Category statistics

### Manual Generation

Generate a weekly report locally:

```bash
# Generate and send email
python weekly_report.py

# Generate without email
python weekly_report.py --no-email

# Analyze specific number of days
python weekly_report.py --days 14
```

Reports are saved to `reports/weekly/weekly-YYYY-MM-DD.md`

## Indie Opportunity Analysis

Every daily run generates `analysis/daily/{date}-indie.md` — a report designed for solo builders evaluating whether a trending product represents a replicable opportunity.

### How it works

1. **Filter** — removes B2B products (enterprise, churn, SSO, CRM), overly complex domains (blockchain, hardware), institutional tools, and GitHub libraries (detected by install commands like `npm install`)
2. **Score** — rates each remaining product 1–5 on four dimensions:
   - `tech_difficulty` — how hard is it to build?
   - `user_acquisition` — how naturally does it spread?
   - `revenue_potential` — how monetisable is the niche?
   - `indie_friendly` — can a solo developer ship and maintain it?
3. **Deep-dive** — the top 5 products each get an 8-question analysis:

| # | Question |
|---|----------|
| 1 | Who are the users? (persona + B2C/B2B) |
| 2 | Why do they need it? (pain point + product's own words) |
| 3 | How does it find users? (distribution channel) |
| 4 | Does it make money? How much? (model + revenue estimate) |
| 5 | What can I learn? (positioning insights) |
| 6 | One-sentence pitch |
| 7 | Can I build it? (technical feasibility) |
| 8 | How do I find users? (specific tactics) |

Each analysis ends with a **💡 First Step** — one concrete action to validate or start building.

### Domain awareness

The analyzer detects 14 product domains from the actual description (fortune telling, browser extension, image generation, developer tool, productivity, etc.) and tailors every answer to that domain — rather than generating generic advice.

### Reports location

```
analysis/daily/
└── 2026-03-18-indie.md   ← auto-committed by GitHub Actions daily
```

## Project Structure

```
trend-monitor/
├── main.py                 # Daily report entry point
├── weekly_report.py        # Weekly report entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── .gitignore
├── README.md
├── CHANGELOG.md
│
├── collectors/            # Data collection modules
│   ├── __init__.py
│   ├── github_trending.py
│   ├── product_hunt.py
│   ├── hackernews.py
│   ├── theresanaiforthat.py
│   ├── chrome_extensions.py
│   └── toolify.py         # Playwright-based (bypasses Cloudflare)
│
├── reporters/             # Report generation
│   ├── __init__.py
│   ├── report_generator.py
│   ├── weekly_report_generator.py
│   └── html_generator.py  # Dark-theme HTML dashboard
│
├── senders/               # Email delivery
│   ├── __init__.py
│   └── email_sender.py
│
├── storage/               # Data persistence
│   ├── __init__.py
│   └── data_store.py
│
├── analyzers/             # Analysis modules
│   ├── __init__.py
│   ├── weekly_analyzer.py
│   └── indie_analyzer.py  # Indie opportunity scoring & deep-dive
│
├── data/                  # Daily data storage
│   └── daily/
│       └── YYYY-MM-DD.json
│
├── docs/                  # GitHub Pages output
│   └── index.html         # HTML dashboard (auto-updated daily)
│
├── analysis/              # Indie opportunity analysis
│   └── daily/
│       └── YYYY-MM-DD-indie.md
│
├── reports/               # Generated reports
│   └── weekly/
│       └── weekly-YYYY-MM-DD.md
│
└── .github/
    └── workflows/
        ├── daily-report.yml
        └── weekly-report.yml
```

## Example Output

```markdown
# AI/Tech Daily Trend Report

**Generated**: 2026-03-17 07:00 (PDT)

---

## Product Hunt - Today's Hot Products

### 1. [AI Assistant Pro](https://www.producthunt.com/posts/ai-assistant-pro)

- **Tagline**: Your personal AI productivity companion

---

## Toolify - AI Tools

### Latest

1. **[PUNK](https://www.toolify.ai/tool/punk-remote-control-for-claude-code)** - Mobile remote control for local Claude Code AI agents.

### Trending

1. **[Claude 2](https://www.toolify.ai/tool/claude-2)** - Claude is an AI assistant from Anthropic.
   - Monthly visits: 290.3M | Growth rate: 43.07%

---

## There's An AI For That - New Tools

### 1. [ImageGen AI](https://theresanaiforthat.com/ai/imagegen-ai/)

- **Description**: Create stunning images from text prompts instantly
- **Category**: Images

---

## Chrome Extensions - Trending

### 1. [Compose AI](https://chromewebstore.google.com/detail/compose-ai/...)

- **Description**: Accelerate your writing with AI
- **Installs**: 300,000 users | **Rating**: 4.8/5.0

---

## GitHub Trending

### 1. [anthropics/claude-code](https://github.com/anthropics/claude-code)

- **Description**: Claude's official coding assistant
- **Stars today**: 1,234 stars today

---

## Hacker News - Top Stories

### 1. [Show HN: I built an open-source AI tool](https://news.ycombinator.com/item?id=12345)

- **Author**: developer123
- **Score**: 456 points | **Comments**: 89
```

### Weekly Report Example

```markdown
# AI/Tech Weekly Trend Report

**Period**: 2026-01-25 to 2026-01-31 (7 days of data)
**Generated**: 2026-01-31 22:00 (PST)

---

## Weekly Overview

- **Total items monitored**: 210
- Product Hunt: 35 (28 unique)
- Toolify Trending: 70 (60 unique)
- AI Tools: 35 (30 unique)
- Chrome Extensions: 35 (32 unique)
- GitHub Projects: 35 (33 unique)
- Hacker News: 35 (31 unique)

---

## Top Keywords This Week

1. **AI** - appeared 15 times
2. **automation** - appeared 12 times
3. **productivity** - appeared 10 times

---

## Repeated Appearances (Sustained Momentum)

### Product Hunt

1. **[AI Writer Pro](link)** - appeared 3 times
   - Description: AI writing assistant
   - First seen: Jan 26
   - Last seen: Jan 30
```

## Troubleshooting

### Gmail Authentication Failed

**Error**: `SMTPAuthenticationError`

**Solutions**:
- Ensure 2-Step Verification is enabled
- Generate a new App Password
- Check that you're using the App Password, not your regular Gmail password
- Verify there are no spaces in the password (or remove them)

### Product Hunt Returns Empty

**Cause**: Product Hunt has rate limiting

**Solution**: The script uses RSS feed which has more lenient limits. If issues persist, wait and retry later.

### GitHub Actions Not Running

**Possible causes**:
- Repository has been inactive for 60+ days
- Workflow file has syntax errors
- Secrets not configured properly

**Solution**:
- Make a commit to reactivate the repository
- Check the Actions tab for error messages
- Verify all secrets are set correctly

### Hacker News API Timeout

**Cause**: HN API can be slow under heavy load

**Solution**: The script has built-in timeout handling. Failed requests are skipped gracefully.

### Toolify Returns Empty / Cloudflare Blocked

**Cause**: Toolify.ai uses Cloudflare protection that blocks plain HTTP requests

**Solution**: The collector uses Playwright to render the page in a real browser. Make sure Chromium is installed:
```bash
playwright install chromium --with-deps
```
In GitHub Actions this step runs automatically before the script.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Here's how you can help:

1. **Report bugs** - Open an issue describing the problem
2. **Suggest features** - Open an issue with your idea
3. **Submit PRs** - Fork the repo, make changes, and submit a pull request

Please ensure your code follows the existing style and includes appropriate tests.

## Acknowledgments

- [Product Hunt](https://www.producthunt.com) for the RSS feed
- [There's An AI For That](https://theresanaiforthat.com) for AI tool discovery
- [Chrome Web Store](https://chromewebstore.google.com) for extension data
- [GitHub](https://github.com) for the trending page
- [Hacker News](https://news.ycombinator.com) for the open API
- [Toolify.ai](https://www.toolify.ai) for AI tool trending data
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Playwright](https://playwright.dev/python/) for browser automation

---

Made with coffee and curiosity.
