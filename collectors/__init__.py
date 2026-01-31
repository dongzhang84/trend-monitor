"""数据采集器模块"""

from .github_trending import fetch_trending_repos
from .product_hunt import fetch_product_hunt_posts
from .hackernews import fetch_hackernews_posts

__all__ = ["fetch_trending_repos", "fetch_product_hunt_posts", "fetch_hackernews_posts"]
