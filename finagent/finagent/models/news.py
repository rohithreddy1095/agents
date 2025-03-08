import datetime
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field

class ArticleModel(BaseModel):
    """Model for a news article."""
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    source: Optional[Dict[str, Optional[str]]] = None
    published_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, article_dict: Dict[str, Any]) -> 'ArticleModel':
        """Create an ArticleModel from a dictionary."""
        return cls(
            title=article_dict.get('title', 'No title'),
            description=article_dict.get('description'),
            content=article_dict.get('content'),
            url=article_dict.get('url'),
            source=article_dict.get('source'),
            published_at=article_dict.get('publishedAt')
        )
    
    def to_text(self) -> str:
        """Convert article to a text representation."""
        parts = [
            f"Title: {self.title}",
            f"Source: {self.source.get('name', 'Unknown source') if self.source else 'Unknown source'}",
            f"Date: {self.published_at or 'Unknown date'}",
            f"URL: {self.url or 'No URL'}"
        ]
        
        if self.description:
            parts.append(f"Description: {self.description}")
        
        if self.content:
            parts.append(f"Content: {self.content}")
            
        return "\n".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert article to a dictionary for JSON serialization."""
        return {
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "url": self.url,
            "source": self.source,
            "published_at": self.published_at
        }
