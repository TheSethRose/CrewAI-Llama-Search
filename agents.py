from crewai import Agent
from src.settings import CrewSettings

# Initialize settings from .env
settings = CrewSettings()

class BaseAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            llm=settings.llm,
            verbose=True,
            allow_delegation=True,
            **kwargs
        )

# Define your first agent
assistant = BaseAgent(
    role="AI Assistant",
    goal="Help users by providing clear and accurate responses",
    backstory="A helpful AI assistant designed to understand and respond to user queries effectively"
)
