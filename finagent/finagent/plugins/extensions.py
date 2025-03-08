"""
Extensions plugin for finagent - registers additional providers and functionality.
"""

from finagent import hookspecs
from finagent.providers.gnews_api import fetch_articles

@hookspecs.hookimpl
def register_news_provider(register):
    """
    Register the GNews API provider with the finagent system.
    
    Args:
        register: Function to register a provider with a name
    """
    register(name="gnews", provider=fetch_articles)