from finagent import hookspecs
from finagent.providers.news_api import fetch_articles
from finagent.providers.openai import generate_summary

# Define a hook implementation using a marker
@hookspecs.hookimpl
def register_news_provider(register):
    """Register the default news provider (NewsAPI)."""
    register(name="newsapi", provider=fetch_articles)