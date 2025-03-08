import sys
import os
import json
import click
from datetime import datetime
from typing import Optional, List, Dict, Any

from finagent.providers import fetch_articles, fetch_articles_with_raw_news_api, fetch_articles_with_raw_gnews
from finagent.models import ArticleModel
from finagent.utils import get_config, set_config
from finagent.raw_storage import store_raw_responses, get_available_stocks, load_raw_responses, merge_responses
from finagent.processors import process_articles

def merge_processed_data(
    filename: str, 
    company_name: str, 
    processed_data: Dict[str, Any]
) -> str:
    """
    Merge new processed data with existing data for a company.
    
    This function checks if there's existing processed data for the company, and if so,
    it merges the new data with the existing one, preserving historical data.
    If no existing data is found, it creates a new file with just the new data.
    
    Args:
        filename: Path to the output file.
        company_name: The company name or ticker symbol.
        processed_data: The processed data to be merged.
        
    Returns:
        The path to the updated JSON file.
    """
    # Check if file exists
    if os.path.exists(filename):
        try:
            # Read existing data
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            
            # Create a new entry with the current data
            new_entry = {
                "company": processed_data.get("company", company_name),
                "article_count": processed_data.get("article_count", 0),
                "timestamp": processed_data.get("timestamp", datetime.now().isoformat()),
                "articles": processed_data.get("articles", [])
            }
            
            # If there's no "history" key yet, create it with the existing data as the first entry
            if "history" not in existing_data:
                # The existing structure is a single entry, move it to history
                history_entry = {
                    "company": existing_data.get("company", company_name),
                    "article_count": existing_data.get("article_count", 0),
                    "timestamp": existing_data.get("timestamp", "unknown"),
                    "articles": existing_data.get("articles", [])
                }
                existing_data["history"] = [history_entry]
            
            # Add the new entry to the history
            existing_data["history"].append(new_entry)
            
            # Update the main data with the new processed articles
            existing_data["company"] = company_name
            existing_data["article_count"] = processed_data.get("article_count", 0)
            existing_data["timestamp"] = processed_data.get("timestamp", datetime.now().isoformat())
            existing_data["articles"] = processed_data.get("articles", [])
            
            # Write the updated data back to the file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
                
            return filename
            
        except (json.JSONDecodeError, KeyError) as e:
            # If there's an error reading the existing file, log it and create a new file
            print(f"Error merging with existing processed data for {company_name}: {e}")
            # Fall through to create a new file
    
    # If file doesn't exist or there was an error, create a new file
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    
    # Write the data to the file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)
    
    return filename

@click.group()
@click.version_option()
def cli():
    """FinAgent: Financial news agent for collecting and analyzing financial data."""
    pass

@cli.command("fetch-news")
@click.option("--company", "-c", required=True, help="Company name or ticker symbol")
@click.option("--limit", default=5, help="Maximum number of articles to fetch", type=int)
@click.option("--raw-dir", help="Directory to store raw API responses", default=None)
def fetch_news_command(company, limit, raw_dir):
    """Fetch news for a specific company using NewsAPI."""
    try:
        click.echo(f"Fetching news for {company} from NewsAPI...")
        articles, raw_data = fetch_articles_with_raw_news_api(company, limit)
        
        if not articles:
            click.echo(f"No articles found for {company}.")
            return
            
        click.echo(f"Found {len(articles)} articles.")
        
        # Store raw responses
        raw_file_path = merge_responses(company, newsapi_response=raw_data, directory=raw_dir)
        click.echo(f"Raw response stored at: {raw_file_path}")
        
        # Display article titles
        for i, article in enumerate(articles, 1):
            click.echo(f"\n{i}. {article.title}")
            click.echo(f"   Source: {article.source.get('name', 'Unknown') if article.source else 'Unknown'}")
            click.echo(f"   URL: {article.url}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command("fetch-gnews")
@click.option("--company", "-c", required=True, help="Company name or ticker symbol")
@click.option("--limit", default=10, help="Maximum number of articles to fetch", type=int)
@click.option("--language", default="en", help="Language code (e.g., en, fr)")
@click.option("--country", default="us", help="Country code (e.g., us, in)")
@click.option("--raw-dir", help="Directory to store raw API responses", default=None)
def fetch_gnews_command(company, limit, language, country, raw_dir):
    """Fetch news for a specific company using Google News API."""
    try:
        click.echo(f"Fetching news for {company} from Google News API...")
        articles, raw_data = fetch_articles_with_raw_gnews(
            company, 
            limit=limit,
            language=language,
            country=country
        )
        
        if not articles:
            click.echo(f"No articles found for {company}.")
            return
            
        click.echo(f"Found {len(articles)} articles.")
        
        # Store raw responses
        raw_file_path = merge_responses(company, gnews_response=raw_data, directory=raw_dir)
        click.echo(f"Raw response stored at: {raw_file_path}")
        
        # Display article titles
        for i, article in enumerate(articles, 1):
            click.echo(f"\n{i}. {article.title}")
            click.echo(f"   Source: {article.source.get('name', 'Unknown') if article.source else 'Unknown'}")
            click.echo(f"   URL: {article.url}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command("process")
@click.option("--company", "-c", required=True, help="Company name or ticker symbol")
@click.option("--raw-dir", help="Directory to read raw API responses from", default=None)
@click.option("--output", "-o", help="Output JSON file path", default=None)
def process_command(company, raw_dir, output):
    """Process stored news for a specific company and save as JSON without analysis."""
    try:
        # Load raw responses
        try:
            data = load_raw_responses(company, directory=raw_dir)
        except FileNotFoundError:
            click.echo(f"No stored data found for {company}. Please fetch news first.")
            sys.exit(1)
            
        # Extract articles from both sources
        newsapi_articles = []
        if "newsapi" in data and "articles" in data["newsapi"]:
            for article in data["newsapi"]["articles"]:
                newsapi_articles.append(ArticleModel.from_dict(article))
                
        gnews_articles = []
        if "gnews" in data and "articles" in data["gnews"]:
            for article in data["gnews"]["articles"]:
                # Convert GNews format to ArticleModel format
                article_data = {
                    'title': article.get('title', 'No title'),
                    'description': article.get('description'),
                    'content': article.get('content'),
                    'url': article.get('url'),
                    'source': {'name': article.get('source', {}).get('name', 'Unknown')},
                    'publishedAt': article.get('publishedAt')
                }
                gnews_articles.append(ArticleModel.from_dict(article_data))
                
        # Combine articles from both sources
        articles = newsapi_articles + gnews_articles
        
        if not articles:
            click.echo(f"No articles found in stored data for {company}.")
            sys.exit(1)
            
        click.echo(f"Found {len(articles)} articles for {company}.")
        
        # Process articles using the processor module
        processed_articles = process_articles(articles, company)
        click.echo(f"Processed {len(processed_articles)} articles.")
        
        # Save processed articles to JSON
        
        # Convert articles to dict for JSON serialization
        articles_data = [article.to_dict() for article in processed_articles]
        processed_data = {
            "company": company,
            "article_count": len(articles),
            "timestamp": datetime.now().isoformat(),
            "articles": articles_data
        }
        
        if not output:
            # Create a default directory for processed data, similar to raw data
            processed_dir = os.path.join(os.getcwd(), "data", "processed")
            # Ensure the directory exists
            os.makedirs(processed_dir, exist_ok=True)
            # Use the same filename convention as raw data
            output = os.path.join(processed_dir, f"{company.upper()}.json")
        
        # Save to JSON using merge_processed_data function
        output_path = merge_processed_data(output, company, processed_data)
            
        click.echo(f"Processed data saved to {output_path}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command("show-news")
@click.option("--company", "-c", required=True, help="Company name or ticker symbol")
@click.option("--raw-dir", help="Directory to read raw API responses from", default=None)
@click.option("--source", type=click.Choice(["all", "newsapi", "gnews"]), default="all", 
              help="News source to display")
def show_news_command(company, raw_dir, source):
    """Show stored news for a specific company."""
    try:
        # Load raw responses
        try:
            data = load_raw_responses(company, directory=raw_dir)
        except FileNotFoundError:
            click.echo(f"No stored data found for {company}. Please fetch news first.")
            sys.exit(1)
            
        if source in ["all", "newsapi"] and "newsapi" in data:
            if "articles" in data["newsapi"]:
                articles = data["newsapi"]["articles"]
                click.echo(f"\n=== NewsAPI Articles ({len(articles)}) ===")
                for i, article in enumerate(articles, 1):
                    click.echo(f"\n{i}. {article.get('title', 'No title')}")
                    click.echo(f"   Source: {article.get('source', {}).get('name', 'Unknown')}")
                    click.echo(f"   Published: {article.get('publishedAt', 'Unknown')}")
                    click.echo(f"   URL: {article.get('url', 'No URL')}")
                    if article.get('description'):
                        click.echo(f"   Description: {article['description']}")
            else:
                click.echo("No NewsAPI articles found.")
                
        if source in ["all", "gnews"] and "gnews" in data:
            if "articles" in data["gnews"]:
                articles = data["gnews"]["articles"]
                click.echo(f"\n=== Google News Articles ({len(articles)}) ===")
                for i, article in enumerate(articles, 1):
                    click.echo(f"\n{i}. {article.get('title', 'No title')}")
                    click.echo(f"   Source: {article.get('source', {}).get('name', 'Unknown')}")
                    click.echo(f"   Published: {article.get('publishedAt', 'Unknown')}")
                    click.echo(f"   URL: {article.get('url', 'No URL')}")
                    if article.get('description'):
                        click.echo(f"   Description: {article['description']}")
            else:
                click.echo("No Google News articles found.")
                
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command("list-companies")
@click.option("--raw-dir", help="Directory to read raw API responses from", default=None)
def list_companies_command(raw_dir):
    """List companies with stored news data."""
    try:
        companies = get_available_stocks(directory=raw_dir)
        
        if not companies:
            click.echo("No stored data found for any company.")
            return
            
        click.echo(f"Found data for {len(companies)} companies:")
        for company in companies:
            click.echo(f"- {company}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command("config")
@click.argument("action", type=click.Choice(["get", "set"]), required=False)
@click.argument("key", required=False)
@click.argument("value", required=False)
def config_command(action, key, value):
    """Get or set configuration values."""
    # If no action is specified, default to "get"
    if not action:
        action = "get"
        
    if action == "get":
        if key:
            config = get_config()
            if key in config:
                click.echo(f"{key}: {config[key]}")
            else:
                click.echo(f"Key '{key}' not found in configuration.")
        else:
            # Display all configuration
            config = get_config()
            for k, v in config.items():
                click.echo(f"{k}: {v}")
    elif action == "set":
        if not key or not value:
            click.echo("Both key and value are required for set action.")
            sys.exit(1)
            
        set_config(key, value)
        click.echo(f"Set {key} to {value}.")


if __name__ == "__main__":
    cli()