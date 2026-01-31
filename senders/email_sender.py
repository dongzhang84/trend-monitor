"""邮件发送器"""

import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv


def send_email_report(report_content, subject=None):
    """发送邮件报告

    Args:
        report_content: 报告内容（Markdown格式）
        subject: 邮件主题（可选，默认为日报主题）
    """
    load_dotenv()

    # 读取配置
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    recipient_email = os.getenv("EMAIL_RECEIVER")

    # 检查必要配置
    if not all([sender_email, sender_password, recipient_email]):
        print("  ⚠️  邮件配置不完整，跳过发送")
        print("     请检查.env文件中的EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER")
        return False

    # 创建邮件主题
    today = datetime.now().strftime("%Y-%m-%d")
    if subject is None:
        subject = f"AI/Tech 趋势日报 - {today}"
    else:
        subject = f"{subject} - {today}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    # 纯文本版本
    text_content = report_content

    # HTML版本（简单转换Markdown）
    html_content = markdown_to_html(report_content)

    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # 发送邮件
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True
    except smtplib.SMTPAuthenticationError:
        print("  ❌ 邮件认证失败，请检查邮箱和密码")
        print("     Gmail用户需要使用应用专用密码")
        return False
    except smtplib.SMTPException as e:
        print(f"  ❌ 邮件发送失败: {e}")
        return False
    except Exception as e:
        print(f"  ❌ 发送错误: {e}")
        return False


def markdown_to_html(md_content):
    """简单的Markdown转HTML"""
    lines = md_content.split("\n")
    html_lines = ["<html><body style='font-family: Arial, sans-serif;'>"]

    for line in lines:
        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2 style='color: #333; border-bottom: 1px solid #ccc;'>{line[3:]}</h2>")
        elif line.startswith("### "):
            # 处理链接
            text = line[4:]
            if "[" in text and "](" in text:
                text = convert_md_links(text)
            html_lines.append(f"<h3 style='margin-bottom: 5px;'>{text}</h3>")
        elif line.startswith("- **"):
            text = line[2:]
            text = text.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
            html_lines.append(f"<p style='margin: 2px 0 2px 20px;'>{text}</p>")
        elif line.startswith("**"):
            text = line.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
            html_lines.append(f"<p>{text}</p>")
        elif line == "---":
            html_lines.append("<hr style='margin: 20px 0;'>")
        elif line.strip():
            html_lines.append(f"<p>{line}</p>")

    html_lines.append("</body></html>")
    return "\n".join(html_lines)


def convert_md_links(text):
    """转换Markdown链接为HTML链接"""
    import re
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.sub(pattern, r'<a href="\2" style="color: #0066cc;">\1</a>', text)
