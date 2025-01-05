"""
Terminal-based Perplexity-like interface for Llama Search.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from typing import Callable, Dict, List, Union
from crewai.crews.crew_output import CrewOutput


class SearchInterface:
    def __init__(self):
        self.console = Console()

    def display_results(self, result: Union[Dict, CrewOutput]):
        """Display the query results, sources, and metadata."""
        self.console.clear()

        # Handle CrewOutput object or dictionary
        if isinstance(result, CrewOutput):
            answer = str(result)
        elif isinstance(result, dict):
            answer = str(result.get("answer", "No answer available"))
        else:
            answer = str(result)

        # Display the answer
        try:
            self.console.print(Panel(Markdown(answer), title="Answer", title_align="left"))
        except TypeError:
            # Fallback to plain text if markdown parsing fails
            self.console.print(Panel(answer, title="Answer", title_align="left"))

        # Display sources if available (for Dict type results)
        if isinstance(result, dict) and result.get("sources"):
            sources = "\n".join([f"- [bold]{src}[/bold]" for src in result["sources"]])
            self.console.print(Panel(sources, title="Sources", title_align="left"))

        # Display metadata (optional, for Dict type results)
        if isinstance(result, dict) and (metadata := result.get("metadata")):
            task_sequence = " → ".join(metadata.get("task_sequence", []))
            self.console.print(Panel(f"Task Sequence: {task_sequence}", title="Metadata", title_align="left"))

    def start(self, process_query: Callable[[str], Union[Dict, CrewOutput]]):
        """Start the search interface."""
        while True:
            query = Prompt.ask("\n[bold]Enter your query (or type 'exit' to quit):[/bold]")
            if query.lower() == "exit":
                break

            result = process_query(query)
            self.display_results(result)
