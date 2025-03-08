import os
import requests
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

from finagent.models import ArticleModel

def fetch_articles(stock_name: str, api_key: Optional[str] = None, limit: int = 5) -> Tuple[List[ArticleModel], Dict[str, Any]]:
    """
    Fetches news articles related to the given stock name using News API.

    Args:
        stock_name (str): The name or ticker symbol of the stock.
        api_key (str, optional): Your News API key. If not provided, it will be read from the environment.
        limit (int, optional): Maximum number of articles to retrieve. Defaults to 5.

    Returns:
        Tuple[List[ArticleModel], Dict[str, Any]]: A tuple containing:
            - A list of article models retrieved from the News API
            - The raw API response as a dictionary
    """
    # Load environment variables if api_key not provided
    if api_key is None:
        load_dotenv()
        api_key = os.getenv("NEWS_API_KEY")
        
    if not api_key:
        raise ValueError("API key is required. Provide it as a parameter or set the NEWS_API_KEY environment variable.")
        
    url = ('https://newsapi.org/v2/everything?'
          f'q={stock_name}&'
          'sortBy=publishedAt&'
          'language=en&'
          f'pageSize={limit}&'
          f'apiKey={api_key}')
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        processed_articles = [ArticleModel.from_dict(article) for article in articles]
        return processed_articles, data
    else:
        error_message = f"Failed to fetch articles: {response.status_code}"
        # If we have an error message in the response, add it
        if response.json and hasattr(response, 'json'):
            try:
                error_data = response.json()
                if "message" in error_data:
                    error_message += f" - {error_data['message']}"
            except:
                pass
        
        raise Exception(error_message)