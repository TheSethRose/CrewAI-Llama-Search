# CrewAI Project Template

A base project setup for running CrewAI locally with Ollama. This template provides a simple starting point for building AI agent-based applications using CrewAI.

## Requirements

- Python 3.x
- [Ollama](https://ollama.ai/) installed and running locally (or accessible via URL)

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Environment Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Configure your environment:
   ```env
   # LLM Configuration (Required)
   OLLAMA_MODEL_NAME=ollama/llama3.3
   OLLAMA_BASE_URL=http://localhost:11434

   # Crew Settings (Optional)
   CREW_VERBOSE=true          # Enable detailed logging output
   CREW_MAX_LOOPS=3          # Maximum number of execution loops
   CREW_CACHE_DIR=./cache    # Directory for caching responses
   CREW_TIMEOUT=300          # Timeout in seconds for operations
   ```

### YAML Configuration

Create a `config` directory and add your agent and task configurations:

1. `config/agents.yaml`:
   ```yaml
   assistant:
     role: "AI Assistant"
     goal: "Demonstrate basic CrewAI functionality with simple responses"
     backstory: "A friendly AI assistant that helps users understand how CrewAI works by providing simple, clear responses"
   ```

2. `config/tasks.yaml`:
   ```yaml
   respond:
     description: "Respond to the user's greeting or basic query"
     expected_output: "A friendly greeting or simple response demonstrating CrewAI functionality"
     tools: []  # No tools needed for this basic example
   ```

## Project Structure

```
├── config/                 # YAML configurations
│   ├── agents.yaml        # Agent definitions
│   └── tasks.yaml         # Task definitions
├── src/
│   └── settings.py        # Environment and settings management
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Example environment configuration
├── agents.py             # Agent setup and initialization
├── crew.py              # Crew and task orchestration
├── main.py              # Application entry point
└── requirements.txt     # Project dependencies
```

## Dependencies

Core dependencies (from requirements.txt):
- crewai
- langchain
- ollama
- langchain-ollama
- python-dotenv
- pydantic
- pydantic-settings
- PyYAML

## Usage

1. Ensure Ollama is running (if using locally)
2. Set up your environment as described in Configuration
3. Run the example:
   ```bash
   python main.py
   ```

The example implements a simple "Hello World" agent that demonstrates basic CrewAI functionality.

## Development

- Environment variables are managed through Pydantic Settings
- Agent and task configurations are loaded from YAML files
- The project uses a modular structure for easy expansion
- Configuration files are gitignored by default

## Customization

1. Modify agent behaviors in `config/agents.yaml`
2. Define new tasks in `config/tasks.yaml`
3. Add tools to tasks as needed
4. Extend the base agent class in `agents.py`
5. Customize crew behavior in `crew.py`
