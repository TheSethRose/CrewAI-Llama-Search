from crewai import Crew, Task
from dotenv import load_dotenv
import yaml
from agents import assistant

# Load environment variables
load_dotenv()

class BasicCrew:
    """A basic template crew for getting started with CrewAI"""

    def __init__(self):
        # Load task configuration
        with open('tasks.yaml', 'r') as f:
            self.tasks_config = yaml.safe_load(f)

        # Create task from config
        self.task = Task(
            **self.tasks_config['respond'],
            agent=assistant
        )

        # Create crew
        self.crew = Crew(
            agents=[assistant],
            tasks=[self.task],
            verbose=True
        )

    def run(self, inputs: dict):
        """Run the crew with the given inputs"""
        return self.crew.kickoff(inputs=inputs)
