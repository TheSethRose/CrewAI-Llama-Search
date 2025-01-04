# Llama Search

A CrewAI-powered research assistant using Llama models, inspired by Perplexity AI.

## Features

- Web search and content extraction
- Source validation and citation management
- Clean, Perplexity-like terminal interface
- Support for both Ollama and OpenAI models
- Configurable agent roles and behaviors

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
poetry run python main.py
```

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

Agents are defined in `agents.yaml`:
```yaml
query_analyzer:
  role: "Query Analysis Specialist"
  goal: "Break down complex queries"
  backstory: "Expert in search optimization..."
```

### Task Configuration

Tasks are defined in `tasks.yaml`:
```yaml
analyze_query:
  description: "Break down user query"
  agent: "query_analyzer"
```

## Development

1. Create a new Poetry environment
```bash
poetry shell
```

2. Follow the setup worksheet
```bash
# Review and customize
cat setup.md
```

3. Implement your changes
4. Run tests (if available)
```bash
poetry run pytest
```

## Project Structure

```
├── pyproject.toml       # Poetry configuration
├── .env                 # Environment variables
├── agents.yaml         # Agent definitions
├── tasks.yaml         # Task definitions
├── main.py           # Entry point
├── agents.py         # Agent initialization
├── crew.py           # Crew orchestration
└── tools/            # Custom tools
    ├── search_tools.py
    ├── scraper_tools.py
    └── citation_tools.py
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
