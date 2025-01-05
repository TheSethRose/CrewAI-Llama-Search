"""
Crew definition for Llama Search.
"""

from crewai import Crew, Task
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LlamaSearchCrew:
    def __init__(self, agents):
        """
        Initialize the Crew for query processing.
        Args:
            agents: A dictionary of initialized agents.
        """
        self.agents = agents
        self.sources = []  # Track sources for each task

        # Define tasks
        self.tasks = [
            Task(
                description="Analyze user query into topics.",
                expected_output="List of topics for searching.",
                agent=agents.get("query_analyzer")  # Use .get() to avoid KeyError
            ),
            Task(
                description="Synthesize a final response from topics.",
                expected_output="A detailed, well-structured answer.",
                agent=agents.get("info_synthesizer")  # Use .get() to avoid KeyError
            )
        ]

        # Initialize Crew
        try:
            self.crew = Crew(
                agents=list(agents.values()),
                tasks=self.tasks,
                verbose=True
            )
            logger.info("Crew initialized successfully with provided agents and tasks.")
        except Exception as e:
            logger.error(f"Error initializing Crew: {e}")
            raise

    def process_query(self, query: str):
        """Run the query through the Crew."""
        logger.info(f"Processing query: {query}")
        try:
            result = self.crew.kickoff(inputs={"query": query})
            logger.debug(f"Query result: {result}")
            task_metadata = [
                {"description": task.description, "agent": task.agent.role if task.agent else "None"}
                for task in self.tasks
            ]
            self.sources = self.collect_sources(result)
            logger.debug(f"Sources collected: {self.sources}")
            return {"result": result, "metadata": task_metadata}
        except Exception as e:
            logger.error(f"Error during query processing: {e}")
            return {"result": f"An error occurred: {e}", "metadata": {}}

    def collect_sources(self, result):
        """Collect sources from tasks or results."""
        sources = []
        for task in self.tasks:
            if task.agent:
                role = getattr(task.agent, "role", "Unknown Role")
                sources.append(role)
            else:
                sources.append("No Agent Assigned")
        logger.debug(f"Collected sources: {sources}")
        return sources

    def validate_agents(self):
        """Validate that all required agents are initialized."""
        required_agents = ["query_analyzer", "info_synthesizer"]
        missing_agents = [agent for agent in required_agents if agent not in self.agents]
        if missing_agents:
            logger.error(f"Missing required agents: {', '.join(missing_agents)}")
            raise ValueError(f"Missing required agents: {', '.join(missing_agents)}")
        logger.info("All required agents are properly initialized.")
