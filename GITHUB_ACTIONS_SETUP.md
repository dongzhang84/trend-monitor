# GitHub Actions 配置指南

本项目使用 GitHub Actions 实现每日自动运行并发送邮件报告。

## 配置步骤

### 1. Fork 或推送代码到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/trend-monitor.git
git push -u origin main
```

### 2. 配置 GitHub Secrets

进入你的 GitHub 仓库，按以下步骤配置：

1. 点击 **Settings** (仓库设置)
2. 左侧菜单选择 **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加以下 Secrets：

| Secret 名称 | 说明 | 示例值 |
|------------|------|--------|
| `EMAIL_SENDER` | 发件人邮箱 | `your-email@gmail.com` |
| `EMAIL_PASSWORD` | 邮箱应用专用密码 | `xxxx xxxx xxxx xxxx` |
| `EMAIL_RECEIVER` | 收件人邮箱 | `your-email@gmail.com` |
| `SMTP_SERVER` | SMTP服务器 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP端口 | `587` |

### 3. Gmail 应用专用密码获取方式

如果使用 Gmail 发送邮件：

1. 登录 [Google 账号](https://myaccount.google.com/)
2. 进入 **安全性** 页面
3. 开启 **两步验证**（如果尚未开启）
4. 在两步验证页面底部，找到 **应用专用密码**
5. 选择应用类型为"邮件"，设备为"其他"
6. 生成的 16 位密码即为 `EMAIL_PASSWORD`

## 运行时间

- **定时运行**: 每天 PST 7:30 (太平洋标准时间)
- **对应 UTC**: 15:30
- **对应北京时间**: 23:30

## 手动触发

如需立即运行测试：

1. 进入仓库的 **Actions** 页面
2. 左侧选择 **Daily Trend Report**
3. 点击 **Run workflow** 按钮
4. 选择分支后点击绿色的 **Run workflow**

## 查看运行结果

1. 进入 **Actions** 页面查看运行历史
2. 点击具体的运行记录查看日志
3. 在 **Artifacts** 部分可下载生成的 `report.md`

## 常见问题

### 邮件发送失败

- 检查 Secrets 配置是否正确
- 确认 Gmail 应用专用密码是否有效
- 查看 Actions 日志中的错误信息

### 定时任务没有运行

- GitHub Actions 的 cron 可能有几分钟延迟
- 确保仓库有最近的活动（60天内）
- 检查 workflow 文件语法是否正确

### 数据采集失败

- 部分网站可能有反爬措施
- 检查 Actions 日志中的具体错误
- 可尝试手动触发重新运行
