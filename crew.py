"""
Crew and task orchestration module.
This module implements the crew setup from setup.md (Section 5: Process Flow).
"""

from crewai import Crew, Task
from dotenv import load_dotenv
import yaml
from agents import assistant

# Load environment variables from .env (Section 6: Implementation Steps)
load_dotenv()

class BasicCrew:
    """
    A basic template crew that implements the process flow from setup.md.
    References Section 5: Process Flow and Section 3: Task Definition.

    The crew configuration includes:
    - Tasks loaded from tasks.yaml (defined in Section 3)
    - Agents from agents.py (defined in Section 2)
    - Process flow defined in Section 5
    """

    def __init__(self):
        # Load task configuration from tasks.yaml
        # References setup.md Section 3: Task Definition
        with open('tasks.yaml', 'r') as f:
            self.tasks_config = yaml.safe_load(f)

        # Create task from config
        # Task configuration maps directly to setup.md Section 3: Task Template
        self.task = Task(
            **self.tasks_config['respond'],  # Maps to Task Name in setup.md
            agent=assistant                  # Maps to Assigned To in setup.md
        )

        # Create crew with defined process flow
        # References setup.md Section 5: Process Flow > Execution Order
        self.crew = Crew(
            agents=[assistant],  # From Section 2: Agent Setup
            tasks=[self.task],   # From Section 3: Task Definition
            verbose=True         # Enables detailed logging
        )

    def run(self, inputs: dict):
        """
        Run the crew with the given inputs.
        References setup.md Section 5: Process Flow > Execution Order.

        Args:
            inputs (dict): Input data for the crew's tasks
                         Format defined in Section 3: Task Definition > Input Requirements

        Returns:
            The crew's output as defined in Section 3: Task Definition > Expected Output
        """
        return self.crew.kickoff(inputs=inputs)
