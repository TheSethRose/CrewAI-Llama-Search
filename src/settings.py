from pydantic_settings import BaseSettings, SettingsConfigDict
from crewai import LLM

class CrewSettings(BaseSettings):
    """Settings for the CrewAI application"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # LLM Configuration
    model_name: str = "ollama/llama3.1"
    base_url: str = "https://llama.sethrose.dev"

    # Internal paths with defaults
    config_path: str = "config"
    agents_yaml: str = "config/agents.yaml"
    tasks_yaml: str = "config/tasks.yaml"

    @property
    def llm(self) -> LLM:
        """Get the configured LLM instance"""
        return LLM(
            model=self.model_name,
            base_url=self.base_url
        )
