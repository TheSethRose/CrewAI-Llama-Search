# Changelog

## [0.1.0] - 2024-03-01

### Added
- Initial project template setup
- Pydantic Settings integration for environment management
- YAML-based configuration for agents and tasks
- Structured project layout with `src/` directory
- Basic CrewAI integration with single agent setup
- Environment configuration with `.env.example`
- Proper `.gitignore` configuration
- Comprehensive README with setup instructions

### Configuration
- Environment variable handling with `OLLAMA_` prefix
- Pydantic settings validation and type safety
- YAML configuration structure for agents and tasks
- Default Ollama model configuration (llama3.3)

### Dependencies
- Core dependencies in requirements.txt:
  - crewai==0.86.0
  - langchain>=0.3.14
  - langchain-ollama==0.2.2
  - ollama==0.4.5
  - pydantic>=2.7.4
  - pydantic-settings>=2.0.0
  - python-dotenv
  - PyYAML

### Project Structure
- `/src` directory for core functionality
- YAML-based configuration in `/config` (gitignored)
- Environment setup with `.env` and `.env.example`
- Core files: agents.py, crew.py, main.py
