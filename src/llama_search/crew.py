"""
Crew configuration for the Llama Search research assistant.
"""

from typing import Dict, List, Optional
from pathlib import Path
import yaml
import logging

from crewai import Crew, Task
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

def create_research_crew(tasks: List[Task]) -> Crew:
    """
    Create a research crew with the specified tasks.

    Args:
        tasks: List of tasks for the crew to perform

    Returns:
        Crew: Configured research crew
    """
    try:
        crew = Crew(
            agents=[
                intent_analyzer,
                query_planner,
                search_agent,
                content_evaluator,
                synthesis_agent
            ],
            tasks=tasks,
            verbose=True
        )

        logger.info("Research crew created successfully")
        return crew

    except Exception as e:
        logger.error(f"Failed to create research crew: {e}")
        raise
