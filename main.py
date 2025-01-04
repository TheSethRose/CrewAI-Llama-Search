#!/usr/bin/env python
"""
Main entry point for the CrewAI project.
This module implements the execution flow defined in setup.md (Section 5: Process Flow).
"""

import warnings
from crew import BasicCrew

# Suppress pysbd warnings
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the basic crew template.
    References setup.md Section 5: Process Flow > Execution Order.

    This function:
    1. Sets up the input query (defined in Section 3: Task Definition > Input Requirements)
    2. Initializes the crew (configured in Section 2: Agent Setup)
    3. Executes the task (defined in Section 3: Task Definition)
    4. Returns the response (format specified in Section 3: Task Definition > Expected Output)
    """
    # Define input query
    # Format specified in setup.md Section 3: Task Definition > Input Requirements
    inputs = {
        'query': 'Hello World! How are you?'  # Basic example query
    }

    # Initialize and run the crew
    # Process flow defined in setup.md Section 5: Process Flow
    BasicCrew().run(inputs=inputs)

if __name__ == "__main__":
    run()
