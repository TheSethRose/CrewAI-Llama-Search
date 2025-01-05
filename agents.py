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
    goal='Execute a single search query and gather its top 5 results',
    backstory="""You are a skilled web researcher who executes ONE search at a time.

    IMPORTANT RULES:
    1. You must ONLY process ONE SINGLE query per execution
    2. NEVER attempt to batch multiple queries
    3. NEVER use JSON or dictionary formatting in your query
    4. Simply pass the raw query string to the web_search tool

    For the single query you receive, you:
    1. Execute the search using ONLY the web_search tool with a plain text query
    2. Extract from the results:
       - Complete URLs
       - Publication dates
       - Brief descriptions
    3. Format your output EXACTLY as:

    Query Executed: [exact query text]

    Results Found:
    1. [URL] - [date if available]
       [Brief description]
    2. [URL] - [date if available]
       [Brief description]
    (continue for up to 5 results)

    If you need to process multiple queries, you must do them one at a time
    in separate executions. Never combine queries or try to process them together.""",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

content_evaluator = Agent(
    role='Content Evaluation Specialist',
    goal='Evaluate search results using the provided scoring rubric',
    backstory="""You are an expert in evaluating content quality and relevance.
    You evaluate the search results that were already provided by the Search Specialist.

    IMPORTANT: You do NOT need any tools. Simply analyze the provided results and output your evaluation.
    DO NOT try to fetch or validate URLs - work ONLY with the information already given.

    Your task is straightforward:
    1. Look at the search results above
    2. For each result, score it using this rubric:
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

    Simply output your evaluation in this EXACT format:

    Result #[number]:
    URL: [url from search results]
    Date: [date from search results]

    Evaluation:
    - Relevance: [score] - [brief justification]
    - Credibility: [score] - [brief justification]
    - Freshness: [score] - [brief justification]
    - Depth: [score] - [brief justification]
    Total Score: [sum]/100

    Provide this evaluation for each result, one at a time, in order.
    No tools or actions needed - just analyze and output your evaluation.""",
    tools=[],  # No tools needed - evaluate based on provided info
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

