from typing import List, Union, Dict, Any

from finagent.models import ArticleModel

def process_articles(articles: List[Union[ArticleModel, Dict[str, Any]]], company_name: str) -> List[ArticleModel]:
    """
    Process news articles without performing any analysis.
    
    Args:
        articles (List[Union[ArticleModel, Dict[str, Any]]]): List of articles to process
        company_name (str): Name of the company these articles are about
        
    Returns:
        List[ArticleModel]: The processed articles
    """
    # Convert any dictionary articles to ArticleModel objects
    article_models = []
    for article in articles:
        if isinstance(article, ArticleModel):
            article_models.append(article)
        else:
            article_models.append(ArticleModel.from_dict(article))
            
    return article_models

