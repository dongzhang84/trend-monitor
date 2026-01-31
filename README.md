# AI/Tech Trend Monitor

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Daily automated monitoring of AI and tech trends from GitHub, Product Hunt, and Hacker News. Get a curated digest delivered to your inbox every morning.

## Features

- **Multi-source Aggregation** - Collects trending data from GitHub, Product Hunt, and Hacker News
- **Automated Reports** - Generates clean Markdown reports with all trending items
- **Email Delivery** - Sends formatted HTML emails directly to your inbox
- **GitHub Actions** - Fully automated daily execution at 7:30 AM PST
- **Zero Cost** - Uses free APIs and GitHub Actions (no paid services required)

## Data Sources

| Source | Data Collected |
|--------|---------------|
| **GitHub Trending** | Repository name, description, daily stars |
| **Product Hunt** | Product name, tagline, product link |
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

The workflow runs automatically at **7:30 AM PST** every day.

To manually trigger the workflow:
1. Go to **Actions** tab
2. Select **Daily Trend Report**
3. Click **Run workflow**

## Project Structure

```
trend-monitor/
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── .gitignore
├── README.md
│
├── collectors/            # Data collection modules
│   ├── __init__.py
│   ├── github_trending.py
│   ├── product_hunt.py
│   └── hackernews.py
│
├── reporters/             # Report generation
│   ├── __init__.py
│   └── report_generator.py
│
├── senders/               # Email delivery
│   ├── __init__.py
│   └── email_sender.py
│
└── .github/
    └── workflows/
        └── daily-report.yml
```

## Example Output

```markdown
# AI/Tech 趋势日报

**生成时间**: 2026-01-30 07:30 (PST)

---

## GitHub Trending

### 1. [anthropics/claude-code](https://github.com/anthropics/claude-code)

- **描述**: Claude's official coding assistant
- **今日Stars**: 1,234 stars today

---

## Product Hunt 今日热门

### 1. [AI Assistant Pro](https://www.producthunt.com/posts/ai-assistant-pro)

- **简介**: Your personal AI productivity companion

---

## Hacker News 热门

### 1. [Show HN: I built an open-source AI tool](https://news.ycombinator.com/item?id=12345)

- **作者**: developer123
- **分数**: 456 points | **评论**: 89
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

- [GitHub](https://github.com) for the trending page
- [Product Hunt](https://www.producthunt.com) for the RSS feed
- [Hacker News](https://news.ycombinator.com) for the open API
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing

---

Made with coffee and curiosity.
