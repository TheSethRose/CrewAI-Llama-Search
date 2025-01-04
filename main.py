#!/usr/bin/env python
import warnings

from crew import BasicCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the basic crew template.
    A simple Hello World example to demonstrate CrewAI functionality.
    """
    inputs = {
        'query': 'Hello World! How are you?'
    }
    BasicCrew().run(inputs=inputs)

if __name__ == "__main__":
    run()
