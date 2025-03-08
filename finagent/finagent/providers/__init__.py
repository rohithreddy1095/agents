from .news_api import fetch_articles as fetch_articles_news_api_raw
from .gnews_api import fetch_articles as fetch_articles_gnews_raw

# Wrapper functions to maintain backward compatibility by returning only articles
def fetch_articles_news_api(stock_name, limit=None, **kwargs):
    """Fetch articles from NewsAPI, returns only the articles without raw data"""
    articles, _ = fetch_articles_news_api_raw(stock_name, limit=limit, **kwargs)
    return articles

def fetch_articles_gnews(stock_name, limit=None, **kwargs):
    """Fetch articles from GNews, returns only the articles without raw data"""
    articles, _ = fetch_articles_gnews_raw(stock_name, limit=limit if limit is not None else 10, **kwargs)
    return articles

# Raw response functions that return (articles, raw_response) tuples
def fetch_articles_with_raw_news_api(stock_name, limit=None):
    """Fetch articles from NewsAPI, returns (articles, raw_response) tuple"""
    return fetch_articles_news_api_raw(stock_name, limit=limit)

def fetch_articles_with_raw_gnews(stock_name, limit=None, **kwargs):
    """Fetch articles from GNews, returns (articles, raw_response) tuple"""
    return fetch_articles_gnews_raw(stock_name, limit=limit if limit is not None else 10, **kwargs)

__all__ = [
    "fetch_articles_news_api",
    "fetch_articles_gnews",
    "fetch_articles_with_raw_news_api",
    "fetch_articles_with_raw_gnews"
]

# For backward compatibility
fetch_articles = fetch_articles_news_api