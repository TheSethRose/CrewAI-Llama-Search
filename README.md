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
   # LLM Provider (Required)
   LLM_PROVIDER=ollama

   # Ollama Configuration
   OLLAMA_MODEL_NAME=llama3.1
   OLLAMA_BASE_URL=http://localhost:11434

   # OpenAI Configuration (if using OpenAI)
   OPENAI_API_KEY=your-api-key-here
   OPENAI_MODEL_NAME=gpt-4o-mini
   ```

### YAML Configuration

The project uses two YAML files for configuration:

1. `agents.yaml`:
   ```yaml
   assistant:
     role: "AI Assistant"
     goal: "Demonstrate basic CrewAI functionality with simple responses"
     backstory: "A friendly AI assistant that helps users understand how CrewAI works by providing simple, clear responses"
   ```

2. `tasks.yaml`:
   ```yaml
   respond:
     description: "Respond to the user's greeting or basic query"
     expected_output: "A friendly greeting or simple response demonstrating CrewAI functionality"
     tools: []  # No tools needed for this basic example
   ```

## Project Structure

```
├── .env                # Environment variables (create from .env.example)
├── .env.example       # Example environment configuration
├── agents.py          # Agent setup and initialization
├── agents.yaml        # Agent definitions
├── crew.py           # Crew and task orchestration
├── main.py           # Application entry point
├── requirements.txt   # Project dependencies
└── tasks.yaml        # Task definitions
```

## Usage

1. Ensure Ollama is running (if using locally)
2. Set up your environment as described in Configuration
3. Run the example:
   ```bash
   python main.py
   ```

The example implements a simple "Hello World" agent that demonstrates basic CrewAI functionality.

## Development

- Environment variables support both Ollama and OpenAI
- Agent and task configurations are loaded from YAML files
- Simple, modular structure for easy customization
- Configuration files are gitignored by default

## Customization

1. Modify agent behaviors in `agents.yaml`
2. Define new tasks in `tasks.yaml`
3. Add custom tools to your agents
4. Extend the base agent class in `agents.py`
5. Customize crew behavior in `crew.py`
