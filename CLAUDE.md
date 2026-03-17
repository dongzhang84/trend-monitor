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
- analyzers/：周报数据分析
- data/daily/：每日采集的原始数据JSON
- reports/weekly/：生成的周报

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

## 开发规则
- 每次修改后跑测试确认不破坏已有功能
- 新增数据源放到 collectors/ 目录
- 报告格式改动放到 reporters/ 目录
