"""
Agent definitions for the Llama Search research assistant.
"""

from typing import Dict, List, Optional
from pathlib import Path
import yaml
import logging
import os
from dotenv import load_dotenv
import json

from crewai import Agent, LLM
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize LLM
def init_llm() -> LLM:
    """Initialize and return LLM based on environment configuration."""
    try:
        llm_provider = os.getenv("LLM_PROVIDER", "openai")
        if llm_provider == "ollama":
            return LLM(
                provider="ollama",
                model=os.getenv("OLLAMA_MODEL_NAME", "llama2")
            )
        elif llm_provider == "openai":
            return LLM(
                provider="openai",
                model=os.getenv("OPENAI_MODEL_NAME", "gpt-4"),
                api_key=os.getenv("OPENAI_API_KEY"),
                api_base=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
            )
        else:
            raise ValueError("LLM_PROVIDER must be 'ollama' or 'openai'")
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        raise

# Initialize tools
def init_search_tool() -> Tool:
    """Initialize and return the web search tool."""
    try:
        search = DuckDuckGoSearchRun()
        return Tool(
            name="web_search",
            func=search.run,
            description="Search the web for recent information. Provide a simple text query."
        )
    except Exception as e:
        logger.error(f"Failed to initialize search tool: {e}", exc_info=True)
        raise

def load_agent_configs() -> Dict:
    """Load agent configurations from YAML file."""
    config_path = Path(__file__).parent / "config" / "agents.yaml"
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)['agents']
    except Exception as e:
        logger.error(f"Failed to load agent configurations: {e}")
        raise

def create_agents(query: str = "") -> Dict[str, Agent]:
    """
    Create and return all agents based on YAML configurations.

    Args:
        query: The user's query to inject into agent configurations
    """
    logger.info(f"Creating agents for query: {query}")
    llm = init_llm()
    search_tool = init_search_tool()
    tool_map = {'web_search': search_tool}

    agents = {}
    configs = load_agent_configs()
    logger.debug(f"Loaded {len(configs)} agent configurations")

    for agent_id, config in configs.items():
        try:
            logger.debug(f"\nCreating agent: {agent_id}")
            logger.debug(f"Original config: {json.dumps(config, indent=2)}")

            # Get tool names from config and map to actual tools
            tool_names = config.get('tools', [])
            tools = [tool_map[name] for name in tool_names if name in tool_map]
            logger.debug(f"Assigned tools: {[t.name for t in tools]}")

            # Format the configuration with the query
            formatted_config = {
                'role': config['role'].format(query=query) if query else config['role'],
                'goal': config['goal'].format(query=query) if query else config['goal'],
                'backstory': config['backstory'].format(query=query) if query else config['backstory']
            }
            logger.debug(f"Formatted config: {json.dumps(formatted_config, indent=2)}")

            # Create agent with configuration
            agent = Agent(
                role=formatted_config['role'],
                goal=formatted_config['goal'],
                backstory=formatted_config['backstory'],
                tools=tools,
                llm=llm,
                verbose=config.get('verbose', True),
                allow_delegation=config.get('allow_delegation', False)
            )
            logger.debug(f"Created agent: {agent_id}")
            logger.debug(f"Agent role: {agent.role}")
            logger.debug(f"Agent goal: {agent.goal}")

            agents[agent_id] = agent

        except Exception as e:
            logger.error(f"Failed to create agent {agent_id}: {e}", exc_info=True)
            raise

    logger.info(f"Successfully created {len(agents)} agents")
    return agents

# Create all agents function
def init_agents(query: str = "") -> Dict[str, Agent]:
    """Initialize all agents with the given query context."""
    try:
        agents = create_agents(query)
        logger.info("All agents initialized successfully")
        return agents
    except Exception as e:
        logger.error(f"Failed to initialize agents: {e}")
        raise

# Initialize agents with empty query first (will be updated per request)
try:
    agents = init_agents()
    # Export individual agents
    intent_analyzer = agents['intent_analyzer']
    query_planner = agents['query_planner']
    search_agent = agents['search_agent']
    content_evaluator = agents['content_evaluator']
    synthesis_agent = agents['synthesis_agent']

    # Export the search tool for direct access if needed
    search_tool = init_search_tool()

    __all__ = [
        'init_agents',  # Export the initialization function
        'intent_analyzer',
        'query_planner',
        'search_agent',
        'content_evaluator',
        'synthesis_agent',
        'search_tool'
    ]

except Exception as e:
    logger.error(f"Failed to initialize agents: {e}")
    raise

def web_search(query: str) -> str:
    """Search the web for information about a specific topic."""
    try:
        search = DuckDuckGoSearchRun()
        results = search.run(query)

        # Format results to include URLs on separate lines
        formatted_results = []
        for i, result in enumerate(results.split('\n\n'), 1):
            if not result.strip():
                continue
            # Extract title and URL if present
            lines = result.split('\n')
            if len(lines) >= 2:
                title = lines[0]
                url = lines[1] if 'http' in lines[1] else 'URL not available'
                formatted_results.append(f"[{i}] {title}\n{url}\n")
            else:
                formatted_results.append(f"[{i}] {result}\n")

        return "\n".join(formatted_results)
    except Exception as e:
        logger.error(f"Search failed: {e}", exc_info=True)
        return f"Error: Search failed - {str(e)}"

