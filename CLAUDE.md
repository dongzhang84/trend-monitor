 # trend-monitor

## 项目说明
AI/Tech 趋势监控工具，自动采集热点数据，生成日报和周报，通过邮件发送。

## 技术栈
- Python
- GitHub Actions（自动化）
- Gmail SMTP（发邮件）

## 项目结构
- main.py：日报入口
- weekly_report.py：周报入口
- collectors/：数据采集模块（6个数据源）
- reporters/：报告生成
- senders/：邮件发送
- storage/：数据持久化
- analyzers/：数据分析模块（周报分析 + indie机会分析）
- data/daily/：每日采集的原始数据JSON
- reports/weekly/：生成的周报
- analysis/daily/：每日 indie 机会分析报告（{date}-indie.md）

## 数据源（按优先级）
1. Product Hunt
2. Toolify.ai（最新工具 + Trending榜单）
3. There's An AI For That
4. Chrome Extensions
5. GitHub Trending
6. Hacker News

## 注意事项
- 环境变量放在 .env，不要提交到 git
- GitHub Actions 定时触发：日报每天 7:00 AM PST，周报每周日 22:00 PST
- 邮件发送用 Gmail App Password，不是账号密码
- 之前踩过坑：Chrome Extensions 用动态搜索而非硬编码ID
- Toolify.ai 有 Cloudflare 保护，必须用 Playwright（requests 会被 403）；需在 Actions 中执行 `playwright install chromium --with-deps`
- Toolify fetch_toolify_tools() 返回 dict {'new': [...], 'trending': [...]}，存储时合并为平铺列表
- collectors/__init__.py 需要显式导出 fetch_toolify_tools，否则 `from collectors import *` 不包含它
- HTML 报告生成到 docs/index.html，由 GitHub Pages 提供访问；daily workflow 每次运行后自动 commit+push
- workflow commit 用 [skip ci] 防止无限循环触发
- collectors 函数名：fetch_product_hunt_posts, fetch_trending_repos, fetch_hackernews_posts（不是 fetch_product_hunt/fetch_github_trending/fetch_hackernews）

## Indie 分析模块（2026-03-18 新增）
- `analyzers/indie_analyzer.py` — 主模块，三个公开函数：`filter_unsuitable_products`, `score_product`, `generate_indie_report`
- 过滤逻辑：B2B关键词、复合短语（analytics+team）、GitHub库检测（npm install等）
- 领域检测：14个领域表，读 name+description（不用tags），驱动8个问题的个性化回答
- 8问框架：用户是谁 / 为什么需要 / 如何找用户 / 商业模式 / 关键洞察 / 一句话Pitch / 能否独立开发 / 如何获客 + 💡第一步行动
- 输出：`analysis/daily/{date}-indie.md`，由 daily workflow 自动 commit
- main.py 集成位置：HTML生成之后、邮件发送之前
- 注意：`generate_indie_report` 的 toolify_data 参数接受 dict({'new':[], 'trending':[]}) 或 list，内部自动处理

## 开发规则
- 每次修改后跑测试确认不破坏已有功能
- 新增数据源放到 collectors/ 目录
- 报告格式改动放到 reporters/ 目录
