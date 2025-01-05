"""
Main script for running the Perplexity-like research assistant.
"""

from crewai import Crew, Task, Process
from agents import (
    intent_analyzer, query_planner,
    search_agent, content_evaluator,
    synthesis_agent, search_tool
)
import logging
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.logging import RichHandler
from rich.markdown import Markdown
import time
import signal

# Configure rich logging - only show important messages
logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, show_time=False, show_path=False)]
)
logger = logging.getLogger(__name__)
console = Console()

def handle_timeout(signum, frame):
    raise TimeoutError("Operation timed out")

def execute_with_timeout(func, timeout=180):
    """Execute a function with a timeout."""
    signal.signal(signal.SIGALRM, handle_timeout)
    signal.alarm(timeout)
    try:
        result = func()
        signal.alarm(0)
        return result
    except TimeoutError:
        return "Error: Operation timed out"
    except Exception as e:
        return f"Error: {str(e)}"

def create_tasks(query: str) -> list:
    """Create task list for processing the query."""
    return [
        Task(
            description=f"Analyze this query and determine the user's intent: '{query}'",
            agent=intent_analyzer,
            expected_output="""Analysis including:
            1. Core information need
            2. Required context/scope
            3. Expected information type
            4. Success criteria"""
        ),
        Task(
            description="Create a list of specific search queries based on the intent analysis",
            agent=query_planner,
            expected_output="""Prioritized list of search queries:
            1. Primary query for main topic
            2. Supporting queries for context
            3. Queries for specific details
            Each with justification."""
        ),
        Task(
            description="Execute each search query and collect top 5 results for each",
            agent=search_agent,
            expected_output="""Process each query one at a time.
            For each individual query, provide:

            Query: [exact query text]
            Results:
            1. [URL] - [date if available]
               [Brief description]
            2. [URL] - [date if available]
               [Brief description]
            (continue for top 5)

            Complete one query fully before moving to the next.
            Do not try to process multiple queries at once."""
        ),
        Task(
            description="Evaluate each search result one at a time. For each result, provide a structured score card:",
            agent=content_evaluator,
            expected_output="""Score card format for each result:
            URL: [full url]
            Relevance: [0-40] - [justification]
            Credibility: [0-30] - [justification]
            Freshness: [0-20] - [justification]
            Depth: [0-10] - [justification]
            Total Score: [sum]/100

            Evaluate one result completely before moving to the next."""
        ),
        Task(
            description="Create a comprehensive summary using only results that scored above 70. Use numbered citations [1], [2], etc.",
            agent=synthesis_agent,
            expected_output="""Final response including:
            1. Clear, structured answer
            2. Numbered citations [1], [2], etc.
            3. Source list with full URLs at the end"""
        )
    ]

def display_agent_action(agent: str, action: str, content: str):
    """Display agent actions in a formatted panel."""
    console.print(Panel(
        Markdown(f"**{action}**\n\n{content}"),
        title=f"[bold cyan]{agent}[/bold cyan]",
        border_style="cyan"
    ))

def process_query(query: str) -> str:
    """Process a search query using the agent crew."""
    tasks = create_tasks(query)

    try:
        # Display initial query
        console.print(Panel(
            f"[bold]{query}[/bold]",
            title="[bold cyan]Processing Query[/bold cyan]",
            border_style="cyan"
        ))

        crew = Crew(
            tasks=tasks,
            process=Process.sequential,
            verbose=True  # Enable verbose output for task tracking
        )

        # Execute tasks with timeout
        result = execute_with_timeout(
            lambda: crew.kickoff({"query": query}),
            timeout=300
        )

        if isinstance(result, str) and result.startswith("Error:"):
            console.print(Panel(
                f"[red]{result}[/red]",
                title="[bold red]Error[/bold red]",
                border_style="red"
            ))
        else:
            # Display final result in a panel
            console.print(Panel(
                Markdown(str(result)),
                title="[bold green]Final Results[/bold green]",
                border_style="green"
            ))

        return str(result)

    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        console.print(Panel(
            f"[red]{error_msg}[/red]",
            title="[bold red]Error[/bold red]",
            border_style="red"
        ))
        return error_msg

def main():
    """Run the main application loop."""
    console.print(Panel(
        "[bold cyan]Perplexity-like Research Assistant[/bold cyan]\n\n"
        "Enter your query below, or type 'exit' to quit.\n"
        "The assistant will perform comprehensive research with source validation.",
        title="Welcome",
        border_style="cyan"
    ))

    while True:
        try:
            query = Prompt.ask("\n[cyan]Enter your query[/cyan] (or type 'exit' to quit)")
            if query.lower() == 'exit':
                console.print(Panel(
                    "[bold cyan]Thank you for using the Research Assistant![/bold cyan]",
                    border_style="cyan"
                ))
                break

            process_query(query)

        except KeyboardInterrupt:
            console.print(Panel(
                "[yellow]Operation cancelled by user[/yellow]",
                border_style="yellow"
            ))
            break
        except Exception as e:
            console.print(Panel(
                f"[red]An error occurred: {str(e)}[/red]",
                title="[bold red]Error[/bold red]",
                border_style="red"
            ))

if __name__ == "__main__":
    main()
