"""
Agent definitions for the Perplexity-like research assistant.
"""

from typing import List, Optional, Dict, Union
from crewai import Agent, LLM, Task
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
import logging
import os
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

__all__ = [
    'intent_analyzer',
    'query_planner',
    'search_agent',
    'content_evaluator',
    'synthesis_agent',
    'search_tool'
]

# Initialize LLM
try:
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    if llm_provider == "ollama":
        llm = LLM(
            provider="ollama",
            model=os.getenv("OLLAMA_MODEL_NAME", "llama2")
        )
    elif llm_provider == "openai":
        llm = LLM(
            provider="openai",
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-4"),
            api_key=os.getenv("OPENAI_API_KEY"),
            api_base=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        )
    else:
        raise ValueError("LLM_PROVIDER must be 'ollama' or 'openai'")

    logger.info(f"LLM initialized successfully for provider: {llm_provider}")
except Exception as e:
    logger.error(f"Failed to initialize LLM: {e}")
    raise

# Initialize tools
def web_search(query: str) -> str:
    """Search the web for information about a specific topic."""
    try:
        search = DuckDuckGoSearchRun()
        result = search.run(query)
        return result
    except Exception as e:
        return f"Error: Search failed - {str(e)}"

# Create tool
search_tool = Tool(
    name="web_search",
    func=web_search,
    description="Search the web for recent information. Provide a simple text query."
)

# Define specialized agents
intent_analyzer = Agent(
    role='Intent Analysis Specialist',
    goal='Understand user queries and determine search strategy',
    backstory="""You are an expert in understanding user intent and information needs.
    You break down queries to understand exactly what information is needed.
    You identify key aspects that need to be researched to provide a complete answer.
    You help formulate effective search strategies.""",
    tools=[],  # No tools needed for analysis
    llm=llm,
    verbose=True
)

query_planner = Agent(
    role='Query Planning Specialist',
    goal='Create effective search queries to gather required information',
    backstory="""You are an expert in formulating search queries.
    You take the analyzed intent and create specific queries to gather needed information.
    You ensure queries are focused and will return relevant results.
    You prioritize queries to get the most important information first.""",
    tools=[],  # No tools needed for planning
    llm=llm,
    verbose=True
)

search_agent = Agent(
    role='Search Specialist',
    goal='Execute individual search queries and gather results one at a time',
    backstory="""You are a skilled web researcher who executes searches methodically.
    For each query you receive, you:

    1. Execute ONE search at a time using the web_search tool
    2. From the results, identify and extract:
       - Complete URLs
       - Publication dates
       - Brief descriptions
    3. Format the output for that single query as:
       Query: [the exact query used]
       Results:
       1. [URL] - [date if available]
          [Brief description]
       2. [URL] - [date if available]
          [Brief description]
       (continue for top 5)

    Important: Only execute ONE query at a time. Do not try to batch queries.
    Wait for each search to complete before moving to the next query.""",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

content_evaluator = Agent(
    role='Content Evaluation Specialist',
    goal='Evaluate and score search results using a systematic scoring rubric',
    backstory="""You are an expert in evaluating content quality and relevance.
    For each search result provided, you:

    1. First read and analyze the content
    2. Then score it across four dimensions:
       - Relevance to query (0-40 points):
         * Direct answer to query: 30-40
         * Partial answer: 15-29
         * Tangentially related: 1-14
       - Source credibility (0-30 points):
         * Major news/academic: 25-30
         * Industry sites: 15-24
         * Blogs/smaller sites: 1-14
       - Information freshness (0-20 points):
         * Within last month: 15-20
         * Within last year: 8-14
         * Older: 1-7
       - Content depth (0-10 points):
         * Comprehensive: 8-10
         * Moderate detail: 4-7
         * Surface level: 1-3

    3. Calculate total score (sum of all dimensions)
    4. For each result, you output:
       URL: [full url]
       Relevance: [score] - [justification]
       Credibility: [score] - [justification]
       Freshness: [score] - [justification]
       Depth: [score] - [justification]
       Total Score: [total]/100

    You evaluate one result at a time, and only use tools when needed to verify information.""",
    tools=[search_tool],  # Needed for fact verification
    llm=llm,
    verbose=True
)

synthesis_agent = Agent(
    role='Information Synthesis Specialist',
    goal='Create comprehensive summaries with proper citations',
    backstory="""You are an expert in synthesizing information and citing sources.
    You take high-scoring results and create clear, accurate summaries.
    You use numbered citations [1], [2], etc., and list sources at the end.
    You ensure all information is properly attributed and verifiable.""",
    tools=[],  # No tools needed for synthesis
    llm=llm,
    verbose=True
)

