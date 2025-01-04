from crewai import Agent
from dotenv import load_dotenv
import os
from crewai import LLM

# Load environment variables
load_dotenv()

def get_llm():
    """Get the configured LLM based on environment settings"""
    provider = os.getenv('LLM_PROVIDER', 'ollama').lower()

    if provider == 'openai':
        return LLM(
            provider="openai",
            model=os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini')
        )
    else:  # default to ollama
        return LLM(
            provider="ollama",
            model=os.getenv('OLLAMA_MODEL_NAME', 'llama3.1'),
            base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        )

class BaseAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(
            llm=get_llm(),
            verbose=True,
            allow_delegation=True,
            **kwargs
        )

# Define your first agent
assistant = BaseAgent(
    role="AI Assistant",
    goal="Demonstrate basic CrewAI functionality with simple responses",
    backstory="A friendly AI assistant that helps users understand how CrewAI works by providing simple, clear responses"
)
