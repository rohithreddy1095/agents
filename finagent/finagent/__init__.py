"""
FinAgent: A financial news agent that fetches and processes financial data.
"""

__version__ = "0.1.0"

from finagent.models import ArticleModel
from finagent.providers import fetch_articles
from finagent.processors import process_articles
from finagent.raw_storage import store_raw_responses

# Define hook specifications for plugins
from . import hookspecs
from . import plugins

# Initialize plugin system
plugins.init_plugin_manager()

__all__ = [
    # Models
    "ArticleModel",
    
    # Core functions
    "fetch_articles",
    "process_articles",
    "store_raw_responses",
]