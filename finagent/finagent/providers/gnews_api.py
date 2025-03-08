import os
import requests
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

from finagent.models import ArticleModel

def fetch_articles(
    stock_name: str, 
    language: str = "en", 
    country: str = "us", 
    limit: int = 10,
    max_results: Optional[int] = None,
    api_key: Optional[str] = None
) -> Tuple[List[ArticleModel], Dict[str, Any]]:
    """
    Fetches news articles related to the given stock name using GNews API.

    Args:
        stock_name (str): The name or ticker symbol of the stock.
        language (str, optional): The language of the news articles. Defaults to "en".
        country (str, optional): The country of the news articles. Defaults to "us".
        limit (int, optional): The maximum number of articles to fetch. Defaults to 10.
        max_results (int, optional): Deprecated. Use limit instead. The maximum number of articles to fetch.
        api_key (str, optional): Your GNews API key. If not provided, it will be read from the environment.

    Returns:
        Tuple[List[ArticleModel], Dict[str, Any]]: A tuple containing:
            - A list of article models retrieved from the GNews API
            - The raw API response as a dictionary
    """
    # Handle deprecated parameter
    if max_results is not None:
        import warnings
        warnings.warn(
            "The 'max_results' parameter is deprecated. Use 'limit' instead.",
            DeprecationWarning,
            stacklevel=2
        )
        limit = max_results
        
    # Load environment variables if api_key not provided
    if api_key is None:
        load_dotenv()
        api_key = os.getenv("GNEWS_API_KEY")
        
    if not api_key:
        raise ValueError("API key is required. Provide it as a parameter or set the GNEWS_API_KEY environment variable.")
        
    url = (
        'https://gnews.io/api/v4/search?'
        f'q={stock_name}&'
        f'lang={language}&'
        f'country={country}&'
        f'max={limit}&'
        f'apikey={api_key}'
    )
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        
        # Transform the GNews articles to match ArticleModel format
        result = []
        for article in articles:
            # GNews has slightly different field names than NewsAPI
            # Map fields to match NewsAPI structure
            article_data = {
                'title': article.get('title', 'No title'),
                'description': article.get('description'),
                'content': article.get('content'),
                'url': article.get('url'),
                'source': {'name': article.get('source', {}).get('name', 'Unknown')},
                'publishedAt': article.get('publishedAt')
            }
            result.append(ArticleModel.from_dict(article_data))
            
        return result, data
    else:
        error_message = f"Failed to fetch articles: {response.status_code}"
        error_data = {}
        # If we have an error message in the response, add it
        if response.json and hasattr(response, 'json'):
            try:
                error_data = response.json()
                if "errors" in error_data:
                    error_message += f" - {error_data['errors']}"
                elif "message" in error_data:
                    error_message += f" - {error_data['message']}"
            except:
                pass
        
        # In case of error, we'll return an empty list and the error data
        # raise Exception(error_message)
        raise Exception(f"{error_message}. Raw response: {error_data}")