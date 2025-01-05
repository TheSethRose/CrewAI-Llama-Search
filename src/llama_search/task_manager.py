"""
Task management and execution for the Llama Search research assistant.
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import yaml
import logging
from datetime import datetime

from crewai import Task
from dotenv import load_dotenv

from .agents import (
    intent_analyzer,
    query_planner,
    search_agent,
    content_evaluator,
    synthesis_agent
)

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class TaskManager:
    """Manages task creation, execution, and result tracking."""

    def __init__(self):
        """Initialize the task manager."""
        self.task_history = []
        self.load_configs()

    def load_configs(self):
        """Load task configurations from YAML."""
        config_path = Path(__file__).parent / "config" / "tasks.yaml"
        try:
            with open(config_path, 'r') as f:
                self.task_configs = yaml.safe_load(f)['tasks']
            logger.info("Task configurations loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load task configurations: {e}")
            raise

    def create_task(self, task_id: str, **kwargs) -> Task:
        """
        Create a task from configuration and additional parameters.

        Args:
            task_id: The identifier of the task in the configuration
            **kwargs: Additional parameters to override configuration

        Returns:
            Task: The created task
        """
        if task_id not in self.task_configs:
            raise ValueError(f"Unknown task ID: {task_id}")

        config = self.task_configs[task_id].copy()
        config.update(kwargs)

        agent_map = {
            'intent_analyzer': intent_analyzer,
            'query_planner': query_planner,
            'search_agent': search_agent,
            'content_evaluator': content_evaluator,
            'synthesis_agent': synthesis_agent
        }

        agent = agent_map[config['agent']]

        task = Task(
            description=config['description'],
            agent=agent,
            context=config['context'],
            expected_output=config['expected_output']
        )

        self.task_history.append({
            'task_id': task_id,
            'timestamp': datetime.now(),
            'config': config
        })

        return task

    def get_task_history(self) -> List[Dict]:
        """
        Get the history of created tasks.

        Returns:
            List[Dict]: List of task creation records
        """
        return self.task_history

    def clear_history(self):
        """Clear the task history."""
        self.task_history = []
        logger.info("Task history cleared")
