"""数据采集器模块"""

from .github_trending import fetch_trending_repos
from .product_hunt import fetch_product_hunt_posts
from .hackernews import fetch_hackernews_posts
from .theresanaiforthat import fetch_ai_tools
from .chrome_extensions import fetch_chrome_extensions

__all__ = [
    "fetch_trending_repos",
    "fetch_product_hunt_posts",
    "fetch_hackernews_posts",
    "fetch_ai_tools",
    "fetch_chrome_extensions",
]
