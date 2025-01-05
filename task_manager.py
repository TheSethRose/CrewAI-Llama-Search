"""
Task management and execution for the research assistant.
"""

import logging
from typing import Any, Dict, List, Optional
from crewai import Crew, Task, Process
from rich.progress import Progress, TaskID
from rich.panel import Panel
from rich.console import Console
from config import APP_CONFIG
from utils import OutputValidator, retry_on_error, format_error

logger = logging.getLogger(__name__)
console = Console()

class TaskManager:
    """Manage task execution and inter-task communication."""

    def __init__(self, progress: Optional[Progress] = None):
        self.progress = progress
        self.results_cache: Dict[str, Any] = {}
        self.validator = OutputValidator()
        self.task_progress_ids: Dict[str, TaskID] = {}

    def add_progress_task(self, task_description: str) -> Optional[TaskID]:
        """Add a progress bar for a task."""
        if self.progress:
            try:
                task_id = self.progress.add_task(
                    f"[green]{task_description}",
                    total=100,
                    start=False
                )
                self.task_progress_ids[task_description] = task_id
                return task_id
            except Exception:
                pass
        return None

    def update_progress(self, task_description: str, advance: int = 1) -> None:
        """Update progress bar if available."""
        if self.progress and task_description in self.task_progress_ids:
            try:
                self.progress.update(self.task_progress_ids[task_description], advance=advance)
            except Exception:
                pass

    def show_conversation(self, role: str, content: str, style: str = "cyan") -> None:
        """Display conversation in a chat-like format."""
        console.print(Panel(
            content,
            title=f"[{style}]{role}[/{style}]",
            title_align="left",
            padding=(1, 2),
            style=style
        ))

    @retry_on_error()
    def execute_research_task(self, task: Task, query: str) -> Dict[str, Any]:
        """Execute research task with validation and progress tracking."""
        try:
            # Show research request
            self.show_conversation(
                "Research Request",
                f"Find information about: {query}"
            )

            # Execute task
            crew = Crew(tasks=[task], process=Process.sequential)
            result = str(crew.kickoff(inputs={"query": query}))

            # Show research response
            self.show_conversation(
                "Research Response",
                result,
                style="green"
            )

            # Validate output
            validated = self.validator.validate_research_output(result)
            if not validated["valid"]:
                raise ValueError(validated["error"])

            # Cache results for next task
            self.results_cache["research"] = validated
            self.update_progress(task.description, advance=100)
            return validated

        except Exception as e:
            logger.error(f"Research failed: {str(e)}")
            raise

    @retry_on_error()
    def execute_writing_task(self, task: Task) -> Dict[str, Any]:
        """Execute writing task with validation and progress tracking."""
        try:
            # Get research results
            research_results = self.results_cache.get("research")
            if not research_results:
                raise ValueError("No research results available")

            # Show writing request
            self.show_conversation(
                "Writing Request",
                "Compose a response using the research findings"
            )

            # Execute task
            crew = Crew(tasks=[task], process=Process.sequential)
            result = str(crew.kickoff(inputs=research_results))

            # Show writing response
            self.show_conversation(
                "Writing Response",
                result,
                style="green"
            )

            # Validate output
            validated = self.validator.validate_writing_output(result)
            if not validated["valid"]:
                raise ValueError(validated["error"])

            self.update_progress(task.description, advance=100)
            return validated

        except Exception as e:
            logger.error(f"Writing failed: {str(e)}")
            raise

    def execute_tasks(self, tasks: List[Task], query: str) -> str:
        """Execute all tasks in sequence with proper error handling."""
        try:
            # Add progress tracking for each task
            for task in tasks:
                self.add_progress_task(task.description)

            # Execute tasks in sequence
            research_result = self.execute_research_task(tasks[0], query)
            writing_result = self.execute_writing_task(tasks[1])

            # Format final output
            return APP_CONFIG["WRITING_FORMAT"].format(
                content=writing_result["content"],
                sources=writing_result["sources"]
            )

        except Exception as e:
            error_msg = format_error("task_failed", str(e), 0, APP_CONFIG["MAX_RETRIES"])
            self.show_conversation("Error", error_msg, style="red")
            return error_msg

    def cleanup(self) -> None:
        """Clean up resources."""
        self.results_cache.clear()
        self.task_progress_ids.clear()
