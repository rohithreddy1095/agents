import os
import json
from typing import Dict, Any, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

def get_client(api_key: Optional[str] = None) -> OpenAI:
    """
    Get an initialized OpenAI client.
    
    Args:
        api_key (str, optional): OpenAI API key. If not provided, it will be read from the environment.
        
    Returns:
        OpenAI: An initialized OpenAI client.
    """
    # Load environment variables if api_key not provided
    if api_key is None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
    if not api_key:
        raise ValueError("API key is required. Provide it as a parameter or set the OPENAI_API_KEY environment variable.")
        
    return OpenAI(api_key=api_key)

def generate_summary(content: str, model: str = "gpt-4o", api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a summary of the provided content using OpenAI.
    
    Args:
        content (str): The content to summarize (typically news articles).
        model (str, optional): The OpenAI model to use. Defaults to "gpt-4o".
        api_key (str, optional): OpenAI API key. If not provided, it will be read from the environment.
        
    Returns:
        Dict[str, Any]: A dictionary containing the summary.
    """
    client = get_client(api_key)
    
    # Create a prompt instructing the model what to extract
    prompt = f"""Summarize and reason out the key information from the following news articles about the stock:

{content}

Output your analysis in strict JSON format with the following structure:
{{
  "summary": "The overall summary of the articles",
  "key_points": ["Point 1", "Point 2", "Point 3"],
  "sentiment": "positive/negative/neutral",
  "potential_impact": "Description of potential market impact"
}}

Ensure your response is valid JSON without any markdown formatting or extra text.
"""
    
    # Call the OpenAI API
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a financial analyst tasked with preprocessing and summarizing news articles about a stock. Extract key information and provide reasoned insights."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    
    # Extract the response content
    summary_text = response.choices[0].message.content.strip()
    
    # Check if the response has JSON markers and extract if needed
    if summary_text.startswith("```json") and summary_text.endswith("```"):
        # Extract JSON content from markdown code block
        summary_text = summary_text.replace("```json", "").replace("```", "").strip()
    
    # Try to parse JSON to validate it
    try:
        summary_dict = json.loads(summary_text)
        return summary_dict
    except json.JSONDecodeError as e:
        # Create a fallback JSON with the raw text
        return {
            "summary": "Error parsing model output",
            "key_points": ["Error in processing articles"],
            "sentiment": "neutral",
            "potential_impact": "Unable to analyze potential impact due to processing error",
            "raw_response": summary_text
        }