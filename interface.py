"""
Terminal-based Perplexity-like interface for Llama Search.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from typing import Callable, Dict, List


class SearchInterface:
    def __init__(self):
        self.console = Console()

    def display_results(self, result: Dict):
        """Display the query results, sources, and metadata."""
        self.console.clear()

        # Display the answer
        self.console.print(Panel(Markdown(result["answer"]), title="Answer", title_align="left"))

        # Display sources if available
        if result.get("sources"):
            sources = "\n".join([f"- [bold]{src}[/bold]" for src in result["sources"]])
            self.console.print(Panel(sources, title="Sources", title_align="left"))

        # Display metadata (optional)
        if metadata := result.get("metadata"):
            task_sequence = " → ".join(metadata.get("task_sequence", []))
            self.console.print(Panel(f"Task Sequence: {task_sequence}", title="Metadata", title_align="left"))

    def start(self, process_query: Callable[[str], Dict]):
        """Start the search interface."""
        while True:
            query = Prompt.ask("\n[bold]Enter your query (or type 'exit' to quit):[/bold]")
            if query.lower() == "exit":
                break

            result = process_query(query)
            self.display_results(result)
