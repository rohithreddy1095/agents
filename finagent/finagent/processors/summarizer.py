from typing import List, Dict, Any, Union

from finagent.models import ArticleModel, SummaryModel
from finagent.providers.openai import generate_summary

def process_and_summarize(articles: List[Union[ArticleModel, Dict[str, Any]]], stock_name: str) -> SummaryModel:
    """
    Process news articles and generate a summary using AI.
    
    Args:
        articles (List[Union[ArticleModel, Dict[str, Any]]]): List of articles to process
        stock_name (str): Name of the stock these articles are about
        
    Returns:
        SummaryModel: A summary of the articles
    """
    # Convert any dictionary articles to ArticleModel objects
    article_models = []
    for article in articles:
        if isinstance(article, ArticleModel):
            article_models.append(article)
        else:
            article_models.append(ArticleModel.from_dict(article))
            
    # Create a combined text from all articles
    combined_text = "\n\n".join([article.to_text() for article in article_models])
    
    # Generate a summary using OpenAI
    summary_data = generate_summary(combined_text)
    
    # Create a SummaryModel from the summary data
    return SummaryModel.from_dict(summary_data, stock_name, article_models)