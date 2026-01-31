"""报告生成器模块"""

from .report_generator import generate_markdown_report
from .weekly_report_generator import generate_weekly_report

__all__ = ["generate_markdown_report", "generate_weekly_report"]
