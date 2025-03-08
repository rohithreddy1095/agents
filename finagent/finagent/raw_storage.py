"""
Module for storing and loading raw API responses from news providers.

This module provides functionality to:
1. Store raw API responses from NewsAPI and GNews in JSON format
2. Load previously saved raw API responses
3. List available stocks with stored raw responses
4. Merge new responses with existing data

The data is structured with "newsapi" and "gnews" as top-level keys,
and saved to files named after the stock symbol (e.g., "AAPL.json").
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List

from finagent.utils.file_utils import ensure_directory_exists


def store_raw_responses(
    stock_name: str,
    newsapi_response: Optional[Dict[str, Any]] = None,
    gnews_response: Optional[Dict[str, Any]] = None,
    directory: Optional[str] = None
) -> str:
    """
    Store raw API responses from NewsAPI and GNews in a JSON file.

    Args:
        stock_name: The stock symbol (e.g., "AAPL").
        newsapi_response: The raw JSON response from NewsAPI.
        gnews_response: The raw JSON response from GNews.
        directory: The directory to store the file. If None, uses a default location.

    Returns:
        The path to the created JSON file.
    """
    # Default to a "raw_data" directory in the current working directory if not specified
    if directory is None:
        directory = os.path.join(os.getcwd(), "data", "raw_data")
    
    # Ensure the directory exists
    ensure_directory_exists(directory)
    
    # Create the filename based on the stock name
    filename = f"{stock_name.upper()}.json"
    filepath = os.path.join(directory, filename)
    
    # Create a structured JSON object with separate sections for each API
    data = {
        "timestamp": datetime.now().isoformat(),
        "stock": stock_name.upper(),
        "newsapi": newsapi_response if newsapi_response is not None else {},
        "gnews": gnews_response if gnews_response is not None else {}
    }
    
    # Write the data to the file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filepath


def load_raw_responses(
    stock_name: str,
    directory: Optional[str] = None
) -> Dict[str, Any]:
    """
    Load raw API responses for a given stock from a JSON file.

    Args:
        stock_name: The stock symbol (e.g., "AAPL").
        directory: The directory where the file is stored. If None, uses the default location.

    Returns:
        A dictionary containing the raw API responses with "newsapi" and "gnews" as keys.
        
    Raises:
        FileNotFoundError: If the file for the specified stock name doesn't exist.
    """
    # Default to a "raw_data" directory in the current working directory if not specified
    if directory is None:
        directory = os.path.join(os.getcwd(), "data", "raw_data")
    
    # Create the filename based on the stock name
    filename = f"{stock_name.upper()}.json"
    filepath = os.path.join(directory, filename)
    
    # Check if file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No raw data found for stock {stock_name} at {filepath}")
    
    # Read the data from the file
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data


def get_available_stocks(directory: Optional[str] = None) -> List[str]:
    """
    Get a list of stock symbols for which raw responses are available.
    
    Args:
        directory: The directory to scan for stock data files. If None, uses the default location.
        
    Returns:
        A list of stock symbols (uppercase) with available raw data.
    """
    # Default to a "raw_data" directory in the current working directory if not specified
    if directory is None:
        directory = os.path.join(os.getcwd(), "data", "raw_data")
    
    # Ensure the directory exists
    if not os.path.exists(directory):
        return []
    
    # Scan for JSON files in the directory
    stock_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    # Extract stock symbols from filenames (removing .json extension)
    stocks = [os.path.splitext(f)[0] for f in stock_files]
    
    return stocks


def merge_responses(
    stock_name: str,
    newsapi_response: Optional[Dict[str, Any]] = None,
    gnews_response: Optional[Dict[str, Any]] = None,
    directory: Optional[str] = None
) -> str:
    """
    Merge new API responses with existing data for a stock.
    
    This function checks if there's existing data for the stock, and if so,
    it merges the new responses with the existing ones, preserving historical data.
    If no existing data is found, it creates a new file with just the new responses.
    
    Args:
        stock_name: The stock symbol (e.g., "AAPL").
        newsapi_response: The raw JSON response from NewsAPI.
        gnews_response: The raw JSON response from GNews.
        directory: The directory to store/read the file. If None, uses a default location.
        
    Returns:
        The path to the updated JSON file.
    """
    # Default to a "raw_data" directory in the current working directory if not specified
    if directory is None:
        directory = os.path.join(os.getcwd(), "data", "raw_data")
    
    # Ensure the directory exists
    ensure_directory_exists(directory)
    
    # Create the filename based on the stock name
    filename = f"{stock_name.upper()}.json"
    filepath = os.path.join(directory, filename)
    
    # Current timestamp
    timestamp = datetime.now().isoformat()
    
    # Check if file exists
    if os.path.exists(filepath):
        try:
            # Read existing data
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            
            # Create a new entry with the current timestamp
            new_entry = {
                "timestamp": timestamp,
                "newsapi": newsapi_response if newsapi_response is not None else {},
                "gnews": gnews_response if gnews_response is not None else {}
            }
            
            # If there's no "history" key yet, create it with the existing data as the first entry
            if "history" not in existing_data:
                # The existing structure is a single entry, move it to history
                history_entry = {
                    "timestamp": existing_data.get("timestamp", "unknown"),
                    "newsapi": existing_data.get("newsapi", {}),
                    "gnews": existing_data.get("gnews", {})
                }
                existing_data["history"] = [history_entry]
            
            # Add the new entry to the history
            existing_data["history"].append(new_entry)
            
            # Update the main data with the new responses
            existing_data["timestamp"] = timestamp
            if newsapi_response is not None:
                existing_data["newsapi"] = newsapi_response
            if gnews_response is not None:
                existing_data["gnews"] = gnews_response
            
            # Write the updated data back to the file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
                
            return filepath
            
        except (json.JSONDecodeError, KeyError) as e:
            # If there's an error reading the existing file, log it and create a new file
            print(f"Error merging with existing data for {stock_name}: {e}")
            # Fall through to create a new file
    
    # If file doesn't exist or there was an error, create a new file
    return store_raw_responses(
        stock_name=stock_name,
        newsapi_response=newsapi_response,
        gnews_response=gnews_response,
        directory=directory
    )