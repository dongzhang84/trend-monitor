"""每日数据存储"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


# 数据存储目录
DATA_DIR = Path(__file__).parent.parent / "data" / "daily"


def save_daily_data(date, data):
    """
    保存每日采集的数据为JSON文件

    Args:
        date: 日期字符串，格式 YYYY-MM-DD
        data: 包含所有数据源的字典

    Returns:
        bool: 保存成功返回True，失败返回False
    """
    try:
        # 确保目录存在
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # 生成时间戳
        pst = ZoneInfo("America/Los_Angeles")
        timestamp = datetime.now(pst).isoformat()

        # 构建完整数据
        full_data = {
            "date": date,
            "timestamp": timestamp,
            "product_hunt": data.get("product_hunt", []),
            "ai_tools": data.get("ai_tools", []),
            "chrome_extensions": data.get("chrome_extensions", []),
            "github_trending": data.get("github_trending", []),
            "hacker_news": data.get("hacker_news", []),
        }

        # 保存文件
        file_path = DATA_DIR / f"{date}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)

        # 保存后清理旧数据
        cleanup_old_data(days=28)

        return True

    except Exception as e:
        print(f"    数据存储失败: {e}")
        return False


def cleanup_old_data(days=28):
    """
    清理指定天数之前的旧数据

    Args:
        days: 保留最近多少天的数据，默认28天（4周）
    """
    try:
        if not DATA_DIR.exists():
            return

        cutoff_date = datetime.now() - timedelta(days=days)

        for file_path in DATA_DIR.glob("*.json"):
            try:
                # 从文件名提取日期
                date_str = file_path.stem  # YYYY-MM-DD
                file_date = datetime.strptime(date_str, "%Y-%m-%d")

                # 删除过期文件
                if file_date < cutoff_date:
                    file_path.unlink()

            except (ValueError, OSError):
                # 跳过无法解析的文件
                continue

    except Exception:
        # 清理失败不影响主流程
        pass


def load_daily_data(date):
    """
    加载指定日期的数据

    Args:
        date: 日期字符串，格式 YYYY-MM-DD

    Returns:
        dict: 数据字典，如果文件不存在返回None
    """
    file_path = DATA_DIR / f"{date}.json"

    if not file_path.exists():
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def list_available_dates(days=7):
    """
    列出最近N天有数据的日期

    Args:
        days: 查询最近多少天

    Returns:
        list: 日期字符串列表，按日期降序排列
    """
    if not DATA_DIR.exists():
        return []

    dates = []
    cutoff_date = datetime.now() - timedelta(days=days)

    for file_path in DATA_DIR.glob("*.json"):
        try:
            date_str = file_path.stem
            file_date = datetime.strptime(date_str, "%Y-%m-%d")

            if file_date >= cutoff_date:
                dates.append(date_str)

        except ValueError:
            continue

    return sorted(dates, reverse=True)
