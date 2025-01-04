"""
Agent configuration and initialization module.
This module implements the agent definitions from setup.md (Section 2: Agent Setup).
"""

from crewai import Agent
from dotenv import load_dotenv
import os
from crewai import LLM

# Load environment variables from .env (Section 6: Implementation Steps)
load_dotenv()

def get_llm():
    """
    Get the configured LLM based on environment settings.
    References setup.md Section 6: Implementation Steps > Environment Setup.

    The LLM provider can be either 'ollama' or 'openai', configured in .env:
    - For Ollama: OLLAMA_MODEL_NAME and OLLAMA_BASE_URL
    - For OpenAI: OPENAI_MODEL_NAME and OPENAI_API_KEY
    """
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
    """
    Base agent class that implements the configuration from setup.md.
    References Section 2: Agent Setup.

    The agent configuration includes:
    - role: From Role Title in setup.md
    - goal: From Objective in setup.md
    - backstory: Combined from Background and Core Functions in setup.md
    - tools: From Tools Needed in setup.md
    """
    def __init__(self, **kwargs):
        super().__init__(
            llm=get_llm(),
            verbose=True,
            allow_delegation=True,
            **kwargs
        )

# Define your first agent based on setup.md Section 2: Agent Setup
# This configuration should match your agents.yaml file
assistant = BaseAgent(
    role="AI Assistant",                    # From Role Title in setup.md
    goal="Demonstrate basic CrewAI functionality with simple responses",  # From Objective
    backstory="A friendly AI assistant that helps users understand how CrewAI works by providing simple, clear responses"  # From Background
)
