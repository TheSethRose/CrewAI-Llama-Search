"""
Crew definition for Llama Search.
"""

from crewai import Crew, Task
import logging

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
        self.crew = Crew(agents=list(agents.values()), tasks=self.tasks, verbose=True)

    def process_query(self, query: str):
        """Run the query through the Crew."""
        result = self.crew.kickoff(inputs={"query": query})
        task_metadata = [{"description": task.description, "agent": task.agent.role if task.agent else "None"} for task in self.tasks]
        self.sources = self.collect_sources(result)
        return {"result": result, "metadata": task_metadata}


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
