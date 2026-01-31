# AI/Tech Trend Monitor

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Daily business opportunity discovery tool - monitors AI products and trending tools from 5 sources. Get a curated digest delivered to your inbox every morning to discover new products and market opportunities.

## Features

- **Multi-source Aggregation** - Collects data from 5 sources: Product Hunt, There's An AI For That, Chrome Extensions, GitHub, Hacker News
- **Automated Reports** - Generates clean Markdown reports with all trending items
- **Weekly Reports** - Automated weekly summaries with trend analysis every Sunday 22:00 PST
- **Email Delivery** - Sends formatted HTML emails directly to your inbox
- **GitHub Actions** - Fully automated daily and weekly execution
- **Zero Cost** - Uses free APIs and GitHub Actions (no paid services required)

## Data Sources

| Source | Data Collected |
|--------|---------------|
| **Product Hunt** | Product name, tagline, product link |
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

The script generates a `report.md` file containing all collected trends, formatted in Markdown.

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

### 3. Schedule

The workflows run automatically:
- **Daily Reports**: 7:30 AM PST (every day)
- **Weekly Reports**: 10:00 PM PST (every Sunday)

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
│   └── chrome_extensions.py
│
├── reporters/             # Report generation
│   ├── __init__.py
│   ├── report_generator.py
│   └── weekly_report_generator.py
│
├── senders/               # Email delivery
│   ├── __init__.py
│   └── email_sender.py
│
├── storage/               # Data persistence
│   ├── __init__.py
│   └── data_store.py
│
├── analyzers/             # Weekly analysis
│   ├── __init__.py
│   └── weekly_analyzer.py
│
├── data/                  # Daily data storage
│   └── daily/
│       └── YYYY-MM-DD.json
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
# AI/Tech 趋势日报

**生成时间**: 2026-01-31 07:30 (PST)

---

## Product Hunt 今日热门

### 1. [AI Assistant Pro](https://www.producthunt.com/posts/ai-assistant-pro)

- **简介**: Your personal AI productivity companion

---

## There's An AI For That - 今日新工具

### 1. [ImageGen AI](https://theresanaiforthat.com/ai/imagegen-ai/)

- **描述**: Create stunning images from text prompts instantly
- **分类**: Images

---

## Chrome Extensions 热门

### 1. [Compose AI](https://chromewebstore.google.com/detail/compose-ai/...)

- **描述**: Accelerate your writing with AI
- **安装量**: 300,000 users | **评分**: 4.8/5.0

---

## GitHub Trending

### 1. [anthropics/claude-code](https://github.com/anthropics/claude-code)

- **描述**: Claude's official coding assistant
- **今日Stars**: 1,234 stars today

---

## Hacker News 热门

### 1. [Show HN: I built an open-source AI tool](https://news.ycombinator.com/item?id=12345)

- **作者**: developer123
- **分数**: 456 points | **评论**: 89
```

### Weekly Report Example

```markdown
# AI/Tech 趋势周报

**统计周期**: 2026-01-25 至 2026-01-31 (共7天数据)
**生成时间**: 2026-01-31 22:00 (PST)

---

## 本周数据概览

- **监测条目总数**: 175 个
- Product Hunt: 35 个 (去重后 28 个)
- AI 工具: 35 个 (去重后 30 个)
- Chrome 扩展: 35 个 (去重后 32 个)
- GitHub 项目: 35 个 (去重后 33 个)
- Hacker News: 35 个 (去重后 31 个)

---

## 本周热门关键词

1. **AI** - 出现 15 次
2. **automation** - 出现 12 次
3. **productivity** - 出现 10 次

---

## 重复出现（持续热度）

### Product Hunt

1. **[AI Writer Pro](link)** - 出现 3 次
   - 描述: AI写作助手
   - 首次发现: 1月26日
   - 最近出现: 1月30日
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
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing

---

Made with coffee and curiosity.
