"""
Web scraping tools for Llama Search.
"""

from typing import Dict, Optional
import requests
from bs4 import BeautifulSoup
import trafilatura
import json

class WebScraperTool:
    """Tool for scraping and cleaning web content."""

    def __init__(self):
        self.name = "web_scraper"
        self.description = "Extract and clean content from web pages"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; LlamaSearch/1.0; +http://example.com)'
        })

    def func(self, url: str) -> str:
        """
        Run the web scraper.

        Args:
            url: The URL to scrape

        Returns:
            JSON string containing:
            - title: Page title
            - text: Main content text
            - metadata: Additional metadata
        """
        try:
            # Download content
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            # Extract clean text using trafilatura
            downloaded = trafilatura.fetch_url(url)
            content = trafilatura.extract(
                downloaded,
                output_format='json',
                include_comments=False,
                include_tables=False
            )

            if content:
                return content

            # Fallback to BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            result = {
                'title': soup.title.string if soup.title else '',
                'text': ' '.join([p.text for p in soup.find_all('p')]),
                'metadata': {}
            }
            return json.dumps(result)

        except Exception as e:
            return json.dumps({
                'error': str(e),
                'title': '',
                'text': '',
                'metadata': {}
            })
