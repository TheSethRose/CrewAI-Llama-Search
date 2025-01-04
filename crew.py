from crewai import Agent, Crew, Process, Task, LLM
from dotenv import load_dotenv
import os
import yaml
from src.settings import CrewSettings

load_dotenv()

class BasicCrew():
    """A basic template crew for getting started with CrewAI"""

    def __init__(self):
        # Initialize settings from .env
        self.settings = CrewSettings()

        # Load configurations
        with open(self.settings.agents_yaml, 'r') as f:
            self.agents_config = yaml.safe_load(f)
        with open(self.settings.tasks_yaml, 'r') as f:
            self.tasks_config = yaml.safe_load(f)

        # Create agent from config
        self.assistant = Agent(
            **self.agents_config['assistant'],
            verbose=True,
            llm=self.settings.llm
        )

        # Create task from config
        self.task = Task(
            **self.tasks_config['respond'],
            agent=self.assistant
        )

        # Create crew
        self.crew = Crew(
            agents=[self.assistant],
            tasks=[self.task],
            process=Process.sequential,
            verbose=True
        )

    def run(self, inputs: dict):
        """Run the crew with the given inputs"""
        return self.crew.kickoff(inputs=inputs)
