"""
Main entry point for the Llama Search research assistant.
"""

from typing import Dict, List, Optional, Any
import logging
from pathlib import Path
import yaml
import sys
import json

from crewai import Task, Crew
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.logging import RichHandler

from .agents import (
    init_agents,
    intent_analyzer,
    query_planner,
    search_agent,
    content_evaluator,
    synthesis_agent
)

# Configure logging with rich
logging.basicConfig(
    level=logging.INFO,  # Set to INFO to reduce noise
    format="%(message)s",  # Simplified format
    handlers=[
        RichHandler(
            rich_tracebacks=True,
            show_time=False,  # Hide timestamp
            show_path=False,  # Hide file path
            markup=True
        )
    ]
)
logger = logging.getLogger(__name__)
console = Console()

# Load environment variables
load_dotenv()

def load_task_configs() -> Dict:
    """Load task configurations from YAML file."""
    config_path = Path(__file__).parent / "config" / "tasks.yaml"
    logger.debug(f"Loading task configurations from: {config_path}")
    try:
        with open(config_path, 'r') as f:
            configs = yaml.safe_load(f)['tasks']
            logger.debug(f"Loaded task configurations: {json.dumps(configs, indent=2)}")
            return configs
    except Exception as e:
        logger.error(f"Failed to load task configurations: {e}", exc_info=True)
        raise

def create_tasks(query: str) -> List[Task]:
    """
    Create tasks based on YAML configurations.

    Args:
        query: The user's query to use in task descriptions
    """
    logger.debug("Creating tasks from configurations")
    configs = load_task_configs()
    agent_map = {
        'intent_analyzer': intent_analyzer,
        'query_planner': query_planner,
        'search_agent': search_agent,
        'content_evaluator': content_evaluator,
        'synthesis_agent': synthesis_agent
    }
    logger.debug(f"Available agents: {list(agent_map.keys())}")

    tasks = []
    task_map = {}  # Store tasks by ID for dependency resolution

    # First pass: Create all tasks
    for task_id, config in configs.items():
        logger.debug(f"\nCreating task: {task_id}")
        logger.debug(f"Task config: {json.dumps(config, indent=2)}")

        try:
            # Format task description with context and query
            context_str = "\n".join([f"- {item}" for item in config['context']])
            description = f"{config['description']}\n\nQuery: {query}\n\nContext:\n{context_str}"

            # Get the agent
            agent = agent_map.get(config['agent'])
            if not agent:
                raise ValueError(f"Unknown agent: {config['agent']}")

            logger.debug(f"Using agent: {agent.role}")
            logger.debug(f"Task description: {description}")
            logger.debug(f"Expected output: {config['expected_output']}")

            task = Task(
                description=description,
                agent=agent,
                expected_output=config['expected_output']
            )
            logger.debug(f"Created task with description: {task.description}")

            tasks.append(task)
            task_map[task_id] = task

        except Exception as e:
            logger.error(f"Failed to create task {task_id}: {e}", exc_info=True)
            raise

    # Second pass: Set up dependencies
    for task_id, config in configs.items():
        if 'dependencies' in config:
            task = task_map[task_id]
            dependencies = [task_map[dep_id] for dep_id in config['dependencies']]
            task.context = dependencies
            logger.debug(f"Set dependencies for task {task_id}: {config['dependencies']}")

    logger.debug(f"Created {len(tasks)} tasks")
    return tasks

def display_agent_thoughts(agent: str, thought: str):
    """Display agent's thought process in a panel."""
    if not thought:
        return

    logger.debug(f"Agent Thought - {agent}: {thought}")

    # Clean up the thought text
    thought_text = thought.replace("Thought:", "").strip()
    if not thought_text:
        return

    console.print(Panel(
        Markdown(thought_text),
        title=f"[bold yellow]{agent}[/bold yellow]",
        subtitle="[yellow]Thought Process[/yellow]",
        border_style="yellow",
        padding=(1, 2)
    ))

def display_agent_task(agent: str, task: str):
    """Display agent's current task in a panel."""
    if not task:
        return

    logger.debug(f"Agent Task - {agent}: {task}")

    # Clean up the task text
    task_text = task.replace("Task:", "").strip()
    if not task_text:
        return

    console.print(Panel(
        Markdown(task_text),
        title=f"[bold blue]{agent}[/bold blue]",
        subtitle="[blue]Current Task[/blue]",
        border_style="blue",
        padding=(1, 2)
    ))

def display_result(result: str):
    """Display research results in a formatted panel."""
    logger.debug("Displaying results")
    console.print(Panel(
        Markdown(str(result)),
        title="[bold green]Research Results[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))

def display_error(error: str):
    """Display error message in a panel."""
    logger.debug(f"Displaying error: {error}")
    console.print(Panel(
        f"[red]{error}[/red]",
        title="[bold red]Error[/bold red]",
        border_style="red"
    ))

def display_welcome():
    """Display welcome message in a panel."""
    welcome_text = """
    Welcome to [bold cyan]Llama Search[/bold cyan]!

    A powerful research assistant that helps you find, validate, and synthesize information.

    - Enter your research query when prompted
    - Type [bold]'exit'[/bold] to quit
    - Press [bold]Ctrl+C[/bold] to cancel a search
    """
    console.print(Panel(welcome_text, title="[bold cyan]Welcome[/bold cyan]", border_style="cyan"))

def process_query(query: str) -> Any:
    """
    Process a research query.

    Args:
        query: The research query to process

    Returns:
        Any: The final research result with citations
    """
    logger.debug(f"Processing query: {query}")
    try:
        # Initialize agents with query context
        logger.info(f"Initializing agents with query: {query}")
        agents_with_context = init_agents(query)

        # Create tasks with query context
        tasks = create_tasks(query)
        logger.debug(f"Created {len(tasks)} tasks for processing")

        # Debug task configurations
        for i, task in enumerate(tasks):
            logger.debug(f"Task {i+1}:")
            logger.debug(f"  Description: {task.description}")
            logger.debug(f"  Agent: {task.agent.role}")
            logger.debug(f"  Expected Output: {task.expected_output}")
            if hasattr(task, 'context') and task.context:
                logger.debug(f"  Dependencies: {[t.description for t in task.context]}")

        # Create crew
        logger.debug("Creating crew with agents and tasks")
        crew = Crew(
            agents=[
                agents_with_context['intent_analyzer'],
                agents_with_context['query_planner'],
                agents_with_context['search_agent'],
                agents_with_context['content_evaluator'],
                agents_with_context['synthesis_agent']
            ],
            tasks=tasks,
            verbose=True,
            step_callback=lambda agent, task, step, input_: handle_step_callback(agent, task, step, input_)
        )

        # Process query
        logger.info("Starting crew kickoff")
        result = crew.kickoff(inputs={'query': query})
        logger.info("Crew processing completed")
        return result

    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise

def handle_step_callback(agent, task, step, input_):
    """Handle crew step callback with detailed logging."""
    try:
        # Log the step details
        logger.debug(f"\nStep Details:")
        logger.debug(f"Agent: {getattr(agent, 'role', 'Unknown') if agent else 'Unknown'}")
        logger.debug(f"Task: {getattr(task, 'description', 'Unknown') if task else 'Unknown'}")
        logger.debug(f"Input: {input_}")
        logger.debug(f"Step: {step}")

        # Display the agent's task if we have one
        if agent and task and hasattr(agent, 'role'):
            display_agent_task(agent.role, task.description)

        # If this is a thought step, display it
        if step and "Thought:" in step and agent and hasattr(agent, 'role'):
            display_agent_thoughts(agent.role, step)

        return None  # Callback must return None

    except Exception as e:
        logger.error(f"Error in step callback: {e}", exc_info=True)
        return None

def main():
    """Interactive main function that prompts for queries."""
    logger.info("Starting Llama Search")
    display_welcome()

    while True:
        try:
            query = Prompt.ask("\n[cyan]Enter your query[/cyan]").strip()
            logger.debug(f"Received query: {query}")

            if not query:
                logger.debug("Empty query received")
                console.print("[yellow]Please enter a valid query.[/yellow]")
                continue

            if query.lower() == 'exit':
                logger.info("User requested exit")
                console.print(Panel(
                    "[bold cyan]Thank you for using Llama Search![/bold cyan]",
                    border_style="cyan"
                ))
                break

            console.print(Panel(
                f"[bold]{query}[/bold]",
                title="[bold cyan]Processing Query[/bold cyan]",
                border_style="cyan"
            ))

            result = process_query(query)
            display_result(result)

        except KeyboardInterrupt:
            logger.info("Search cancelled by user")
            console.print(Panel(
                "[yellow]Search cancelled. Enter a new query or type 'exit' to quit.[/yellow]",
                border_style="yellow"
            ))
            continue
        except Exception as e:
            logger.error("Error in main loop", exc_info=True)
            display_error(f"An error occurred: {str(e)}")
            console.print("Please try again or type 'exit' to quit.")
            continue

if __name__ == "__main__":
    main()
