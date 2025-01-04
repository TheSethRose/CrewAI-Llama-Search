"""
Web search tools for Llama Search.
"""

from typing import List, Dict
from duckduckgo_search import DDGS
import json

class WebSearchTool:
    """Tool for performing web searches using DuckDuckGo."""

    def __init__(self):
        self.name = "web_search"
        self.description = "Search the web using DuckDuckGo"
        self.search = DDGS()

    def func(self, query: str, max_results: int = 5) -> str:
        """
        Run the web search.

        Args:
            query: The search query
            max_results: Maximum number of results to return

        Returns:
            JSON string of search results
        """
        results = []

        try:
            for r in self.search.text(query, max_results=max_results):
                results.append({
                    'title': r['title'],
                    'url': r['link'],
                    'snippet': r['body']
                })
        except Exception as e:
            print(f"Search error: {str(e)}")

        return json.dumps(results)
