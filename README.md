# Llama Search

A CrewAI-powered research assistant that performs comprehensive web research with source validation and citation management.

## Features

- Intelligent query analysis and planning
- Web search with source validation
- Content evaluation and scoring
- Citation management and synthesis
- Support for both Ollama and OpenAI models
- YAML-based configuration for agents and tasks
- Interactive query interface

## Prerequisites

- Python 3.10 or higher
- Poetry for dependency management
- Ollama (if using local models) or OpenAI API key

## Quick Start

1. Clone this repository
```bash
git clone https://github.com/yourusername/llama-search.git
cd llama-search
```

2. Install dependencies with Poetry
```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

3. Configure your environment
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

4. Run the application
```bash
poetry run python -m src.llama_search.main
```

The application will prompt you for research queries. Type 'exit' to quit.

## Configuration

### Environment Variables

Configure in `.env`:
```env
# Choose your LLM provider
LLM_PROVIDER=ollama     # or openai

# For Ollama
OLLAMA_MODEL_NAME=llama2
OLLAMA_BASE_URL=http://localhost:11434

# For OpenAI
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL_NAME=gpt-4
```

### Agent Configuration

Agents are defined in `src/llama_search/config/agents.yaml`:
```yaml
intent_analyzer:
  role: Intent Analysis Specialist
  goal: Understand user queries and determine search strategy
  backstory: Expert in understanding user intent...

query_planner:
  role: Query Planning Specialist
  goal: Create effective search queries
  backstory: Expert in formulating search strategies...
```

### Task Configuration

Tasks are defined in `src/llama_search/config/tasks.yaml`:
```yaml
analyze_intent:
  description: Analyze the user's query
  agent: intent_analyzer
  context: Break down the query into searchable components...

plan_queries:
  description: Create search queries
  agent: query_planner
  context: Generate focused search queries...
```

## Project Structure

```
src/
└── llama_search/
    ├── __init__.py
    ├── agents.py          # Agent initialization and management
    ├── main.py           # Entry point
    ├── crew.py           # Crew configuration
    ├── task_manager.py   # Task management
    ├── config/
    │   ├── agents.yaml   # Agent definitions
    │   └── tasks.yaml    # Task definitions
    ├── tools/            # Custom tools
    └── tests/            # Test files
```

## Development

1. Create a new Poetry environment
```bash
poetry shell
```

2. Follow the setup guide
```bash
# Review and customize
cat setup.md
```

3. Run tests (when available)
```bash
poetry run pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Ollama](https://ollama.ai/)
- [Setup Guide](setup.md)
