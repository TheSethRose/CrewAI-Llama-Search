"""
Citation management tools for Llama Search.
"""

from typing import Dict, List
from datetime import datetime
from urllib.parse import urlparse
import json

class CitationManagerTool:
    """Tool for managing and formatting citations."""

    def __init__(self):
        self.name = "citation_manager"
        self.description = "Format and manage source citations"

    def func(self, source_json: str) -> str:
        """
        Run the citation manager.

        Args:
            source_json: JSON string containing source information:
                - title: Page title
                - url: Source URL
                - author: Author name (optional)
                - date: Publication date (optional)

        Returns:
            JSON string containing:
            - citation: Full citation
            - inline: Inline citation
        """
        try:
            source = json.loads(source_json)

            # Extract domain and date
            domain = urlparse(source['url']).netloc
            date = source.get('date', datetime.now().strftime('%Y, %B %d'))

            # Format author
            author = source.get('author', domain)

            # Create citations
            full_citation = f"{author} ({date}). {source['title']}. Retrieved from {source['url']}"
            inline_citation = f"({author}, {date})"

            return json.dumps({
                'citation': full_citation,
                'inline': inline_citation
            })

        except Exception as e:
            return json.dumps({
                'error': str(e),
                'citation': '',
                'inline': ''
            })

    def format_bibliography(self, sources_json: str) -> str:
        """
        Format a bibliography from multiple sources.

        Args:
            sources_json: JSON string containing list of source information

        Returns:
            Formatted bibliography string
        """
        try:
            sources = json.loads(sources_json)
            citations = []

            for source in sources:
                result = json.loads(self.func(json.dumps(source)))
                if 'citation' in result:
                    citations.append(result['citation'])

            return "\n\nReferences\n" + "\n\n".join(citations)

        except Exception as e:
            return f"Error formatting bibliography: {str(e)}"
