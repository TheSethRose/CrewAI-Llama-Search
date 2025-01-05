# Llama Search Setup Guide

This guide helps you set up and configure your Llama Search instance.

## 1. Environment Setup

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Configure your LLM provider in `.env`:

For Ollama:
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL_NAME=llama2
OLLAMA_BASE_URL=http://localhost:11434
```

For OpenAI:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL_NAME=gpt-4
OPENAI_API_BASE=https://api.openai.com/v1
```

## 2. Agent Configuration

Agents are defined in `src/llama_search/config/agents.yaml`. Each agent has a specific role in the research process:

1. Intent Analyzer
   - Understands user queries
   - Identifies key research aspects
   - Determines search strategy

2. Query Planner
   - Creates focused search queries
   - Prioritizes information needs
   - Ensures comprehensive coverage

3. Search Agent
   - Executes web searches
   - Extracts relevant information
   - Formats results consistently

4. Content Evaluator
   - Scores search results
   - Validates sources
   - Applies quality metrics

5. Synthesis Agent
   - Combines information
   - Manages citations
   - Creates final summaries

## 3. Task Configuration

Tasks are defined in `src/llama_search/config/tasks.yaml`. The research process follows these steps:

1. Query Analysis
   - Break down user query
   - Identify main topics
   - Determine constraints

2. Search Planning
   - Create specific queries
   - Prioritize search order
   - Plan information gathering

3. Information Retrieval
   - Execute searches
   - Extract key details
   - Format results

4. Content Evaluation
   - Score results
   - Validate sources
   - Filter quality content

5. Information Synthesis
   - Combine findings
   - Add citations
   - Create summary

## 4. Validation Checklist

Before running queries:

### Environment
- [ ] `.env` file configured
- [ ] LLM provider accessible
- [ ] API keys valid (if using OpenAI)

### Configuration
- [ ] `agents.yaml` syntax valid
- [ ] `tasks.yaml` syntax valid
- [ ] Agent roles properly defined
- [ ] Task flow logical

### Tools
- [ ] Web search functioning
- [ ] DuckDuckGo accessible
- [ ] Error handling working

## 5. Running Tests

When tests are available:
```bash
poetry run pytest
```

## 6. Troubleshooting

Common issues and solutions:

1. LLM Connection
   - Verify API keys
   - Check provider status
   - Confirm model names

2. Web Search
   - Check internet connection
   - Verify DuckDuckGo access
   - Review search limits

3. Configuration
   - Validate YAML syntax
   - Check file paths
   - Verify dependencies

## Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)

