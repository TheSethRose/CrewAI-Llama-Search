# CrewAI Project Template

A streamlined template for building AI agent crews using CrewAI. This template provides a structured approach to defining and implementing your AI agents, tasks, and workflows.

## Quick Start

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure your settings
4. Follow the setup worksheet to plan your implementation
5. Run the example: `python main.py`

## Project Planning

This template includes a comprehensive setup worksheet (`setup.md`) that guides you through planning and implementing your CrewAI project:

1. **Project Overview**: Define your goals and constraints
2. **Agent Setup**: Design your AI agents and their roles
3. **Task Definition**: Specify what your agents will do
4. **Tool Integration**: Configure APIs and custom tools
5. **Process Flow**: Plan how everything works together
6. **Implementation**: Step-by-step setup guide
7. **Validation**: Ensure everything works correctly

### Using the Setup Worksheet

The `setup.md` worksheet helps you:
- Plan your entire project before coding
- Map your plan directly to configuration files
- Ensure all components are properly defined
- Follow CrewAI best practices

Example workflow:
1. Fill out each section in `setup.md`
2. Use the provided examples to create your YAML configs
3. Copy configurations to the appropriate files
4. Follow the implementation checklist
5. Validate your setup

## Project Structure

```
├── .env.example          # Environment variable template
├── .env                  # Your environment configuration
├── setup.md             # Project planning worksheet
├── agents.yaml          # Agent definitions
├── tasks.yaml           # Task definitions
├── main.py             # Entry point
├── agents.py           # Agent initialization
├── crew.py             # Crew setup and execution
└── requirements.txt    # Project dependencies
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:
```env
LLM_PROVIDER=ollama          # or openai
OLLAMA_MODEL_NAME=llama2     # if using Ollama
OPENAI_API_KEY=             # if using OpenAI
```

### Agent Configuration

Define your agents in `agents.yaml`:
```yaml
primary_agent:
  role: "Research Assistant"
  goal: "Analyze market trends"
  backstory: "Expert in data analysis..."
  tools: ["web_search", "data_analysis"]
```

### Task Configuration

Define tasks in `tasks.yaml`:
```yaml
market_analysis:
  description: "Analyze top competitors"
  expected_output: "Detailed comparison report"
  agent: "research_assistant"
```

## Development

1. Plan your project using `setup.md`
2. Configure your environment
3. Define agents and tasks
4. Implement custom tools if needed
5. Test and validate

## Best Practices

- Follow the setup worksheet step by step
- Keep configurations in YAML files
- Test thoroughly before deployment
- Document custom tools and functions

## Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Setup Guide](setup.md)
- [Example Implementations](https://docs.crewai.com/examples/)
