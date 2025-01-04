"""
Main entry point for Llama Search using CrewAI.
"""

from crewai import Crew, Task, Agent, LLM
from interface import SearchInterface
from dotenv import load_dotenv
import os
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

if os.getenv("LLM_PROVIDER") == "ollama":
    if not os.getenv("OLLAMA_MODEL_NAME"):
        logger.warning("OLLAMA_MODEL_NAME not set. Using default 'llama3.1'.")

    if not os.getenv("OLLAMA_BASE_URL"):
        logger.warning("OLLAMA_BASE_URL not set. Using default 'http://localhost:11434'.")

if os.getenv("LLM_PROVIDER") == "openai":
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY not set. Using default 'sk-proj-00000000000000000000000000000000'.")

# Initialize LLM (Llama 3.1)
llm = LLM(
    model=os.getenv("OLLAMA_MODEL_NAME", "llama3.1"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
)

# Define agents
query_analyzer = Agent(
    role="Query Analyzer",
    goal="Break down complex queries into specific, searchable topics.",
    backstory="Expert in query analysis and search optimization.",
    verbose=True,
    llm=llm
)

info_synthesizer = Agent(
    role="Information Synthesizer",
    goal="Combine information into a coherent and comprehensive response.",
    backstory="Skilled in technical writing and information synthesis.",
    verbose=True,
    llm=llm
)

# Define tasks
tasks = [
    Task(
        description="Analyze a query to extract searchable topics.",
        expected_output="A list of topics and keywords to search for.",
        agent=query_analyzer
    ),
    Task(
        description="Synthesize analyzed topics into a comprehensive response.",
        expected_output="A well-structured answer based on topics.",
        agent=info_synthesizer
    )
]

# Create Crew
crew = Crew(
    agents=[query_analyzer, info_synthesizer],
    tasks=tasks,
    verbose=True
)

def process_query(query: str):
    try:
        result = crew.kickoff(inputs={"query": query})
        sources = getattr(crew, "sources", [])
        return {
            "answer": result,
            "sources": sources,
            "metadata": {"task_sequence": [task.description for task in tasks]},
        }
    except Exception as e:
        return {"answer": f"An error occurred: {str(e)}", "sources": [], "metadata": {}}


if __name__ == "__main__":
    # Start the terminal interface
    interface = SearchInterface()
    interface.start(process_query)
