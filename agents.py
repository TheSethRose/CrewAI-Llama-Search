"""
Agent definitions for Llama Search.
"""

from crewai import Agent, LLM
from crewai.project import CrewBase, agent
from dotenv import load_dotenv
import os
import logging
from tools.search_tools import WebSearchTool
from tools.scraper_tools import WebScraperTool
from tools.citation_tools import CitationManagerTool

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Agent configurations
AGENT_CONFIGS = {
    'query_analyzer': {
        'role': 'Query Analysis Specialist',
        'goal': 'Break down and analyze search queries to identify key topics and concepts',
        'backstory': 'Expert in natural language processing and query analysis with years of experience in search optimization'
    },
    'search_specialist': {
        'role': 'Web Search Expert',
        'goal': 'Find relevant and reliable information from various web sources',
        'backstory': 'Experienced web researcher with expertise in advanced search techniques and source evaluation'
    },
    'content_extractor': {
        'role': 'Content Extraction Specialist',
        'goal': 'Extract and process relevant information from web pages',
        'backstory': 'Expert in web scraping and content processing with strong attention to detail'
    },
    'source_validator': {
        'role': 'Source Validation Expert',
        'goal': 'Verify the credibility and reliability of information sources',
        'backstory': 'Experienced fact-checker with expertise in source verification and validation'
    },
    'info_synthesizer': {
        'role': 'Information Synthesis Expert',
        'goal': 'Combine and structure information into coherent and comprehensive responses',
        'backstory': 'Skilled information analyst with expertise in organizing and presenting complex data'
    },
    'citation_specialist': {
        'role': 'Citation Management Expert',
        'goal': 'Manage and format citations for all sources used',
        'backstory': 'Expert in academic citation standards and reference management'
    }
}

# Initialize LLM
llm = LLM(
    model=os.getenv('OLLAMA_MODEL_NAME', 'llama2'),
    base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
    provider="ollama"
)

@CrewBase
class LlamaSearchAgents:
    @agent
    def query_analyzer(self) -> Agent:
        return Agent(
            role=AGENT_CONFIGS['query_analyzer']['role'],
            goal=AGENT_CONFIGS['query_analyzer']['goal'],
            backstory=AGENT_CONFIGS['query_analyzer']['backstory'],
            verbose=True,
            llm=llm
        )

    @agent
    def search_specialist(self) -> Agent:
        return Agent(
            role=AGENT_CONFIGS['search_specialist']['role'],
            goal=AGENT_CONFIGS['search_specialist']['goal'],
            backstory=AGENT_CONFIGS['search_specialist']['backstory'],
            verbose=True,
            llm=llm,
            tools=[WebSearchTool()]
        )

    @agent
    def content_extractor(self) -> Agent:
        return Agent(
            role=AGENT_CONFIGS['content_extractor']['role'],
            goal=AGENT_CONFIGS['content_extractor']['goal'],
            backstory=AGENT_CONFIGS['content_extractor']['backstory'],
            verbose=True,
            llm=llm,
            tools=[WebScraperTool()]
        )

    @agent
    def source_validator(self) -> Agent:
        return Agent(
            role=AGENT_CONFIGS['source_validator']['role'],
            goal=AGENT_CONFIGS['source_validator']['goal'],
            backstory=AGENT_CONFIGS['source_validator']['backstory'],
            verbose=True,
            llm=llm,
            tools=[WebScraperTool()]
        )

    @agent
    def info_synthesizer(self) -> Agent:
        return Agent(
            role=AGENT_CONFIGS['info_synthesizer']['role'],
            goal=AGENT_CONFIGS['info_synthesizer']['goal'],
            backstory=AGENT_CONFIGS['info_synthesizer']['backstory'],
            verbose=True,
            llm=llm
        )

    @agent
    def citation_specialist(self) -> Agent:
        return Agent(
            role=AGENT_CONFIGS['citation_specialist']['role'],
            goal=AGENT_CONFIGS['citation_specialist']['goal'],
            backstory=AGENT_CONFIGS['citation_specialist']['backstory'],
            verbose=True,
            llm=llm,
            tools=[CitationManagerTool()]
        )

# Create instance of agents
agents = LlamaSearchAgents()

# Export individual agents for backward compatibility
query_analyzer = agents.query_analyzer()
search_specialist = agents.search_specialist()
content_extractor = agents.content_extractor()
source_validator = agents.source_validator()
info_synthesizer = agents.info_synthesizer()
citation_specialist = agents.citation_specialist()
