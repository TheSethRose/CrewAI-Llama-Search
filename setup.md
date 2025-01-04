# CrewAI Project Configuration Worksheet

Plan your CrewAI project step-by-step with this worksheet. Each section helps you define your project's goals, agents, tasks, and tools.

---

# Section 1: Project Overview
Define your project's main purpose and constraints.

#### The name of your CrewAI project
Project Name:

#### The main objective your crew will accomplish
Primary Goal:

#### The specific deliverable or result you expect
Expected Output:

#### Any time or resource constraints for the project
Time Constraints:

---

# Section 2: Agent Setup
Agents are your project workers. Start with the **Primary Agent**.

## Primary Agent
#### The specific role or title of the agent (maps to role: in agents.yaml)
Role Title (e.g., Research Assistant):

#### The agent's primary objective (maps to goal: in agents.yaml)
Objective (e.g., Analyze market trends):

#### Key functions this agent will perform (used to craft the backstory: in agents.yaml)
Core Functions (list 2-3 key tasks):
-
-

#### Rate agent expertise from 1-10 (influences temperature setting in agents.yaml)
Expertise Rating (1-10):

#### Agent's background and experience (combines with Core Functions for backstory: in agents.yaml)
Background:

#### List of tools the agent needs access to (becomes tools: list in agents.yaml)
Tools Needed (e.g., web_search, data_analysis):

This maps to agents.yaml as:
```yaml
primary_agent:
  role: "Research Assistant"              # From Role Title
  goal: "Analyze market trends"           # From Objective
  backstory: "Expert in data analysis..." # Combined from Background and Functions
  tools: ["web_search", "data_analysis"]  # From Tools Needed
  temperature: 0.7                        # Based on Expertise Rating
```

## Supporting Agents
Add other agents to assist the primary agent.

#### The role of this supporting agent
Role:

#### The specific goal this agent should achieve
Goal:

#### Key functions this agent will perform
Key Functions:
-
-

#### Tools required for this agent's tasks
Tools Needed:

This maps to agents.yaml as:
```yaml
supporting_agent:
  role: ""        # From Role
  goal: ""        # From Goal
  backstory: ""   # Generated from Functions
  tools: []       # From Tools Needed
```

---

# Section 3: Task Definition
Define specific jobs for your agents.

## Input Requirements
What information or resources each task needs:

#### Name of the task (becomes the YAML key in tasks.yaml)
Task Name:

#### Which agent performs this task (use agent's YAML key from agents.yaml)
Assigned To:

#### Clear description of what needs to be done (maps to description: in tasks.yaml)
Description:

#### What information or resources the task needs (included in description: in tasks.yaml)
Input Requirements:

#### What the task should produce (maps to expected_output: in tasks.yaml)
Expected Output:

#### Specific criteria to consider the task complete (included in expected_output: in tasks.yaml)
Completion Criteria:
- [ ]
- [ ]

Example task configuration:
```yaml
market_analysis:
  description: "Analyze top 5 competitors in the market. Required input: List of competitor names."
  expected_output: "Detailed comparison report including market share analysis, product comparison, and pricing strategy"
  agent: "research_assistant"
  tools: ["web_search", "data_analysis"]
```

---

# Section 4: Tool Integration
List APIs or custom tools your agents need.

## Required APIs
#### List each API needed
API Name:
- Purpose:
- Access Level:
- Environment Variable:

## Custom Functions
#### List each custom function
Function Name:
- Purpose:
- Input:
- Output:
- Location: tools/custom_tools.py

---

# Section 5: Process Flow
Outline how tasks and agents work together.

## Execution Order
Define the sequence of operations:
1.
2.
3.

## Error Management
Define error handling scenarios:
Case 1:
Case 2:

This maps to crew.py as:
```python
class BasicCrew:
    def __init__(self):
        self.crew = Crew(
            agents=[],    # From Section 2: Agent Setup
            tasks=[],     # From Section 3: Task Definition
            verbose=True
        )
```

---

# Section 6: Implementation Steps

## Environment Setup
- [ ] Copy .env.example to .env
- [ ] Configure LLM provider:
  ```env
  LLM_PROVIDER=ollama          # or openai
  OLLAMA_MODEL_NAME=llama2     # if using Ollama
  OPENAI_API_KEY=             # if using OpenAI
  ```

## Agent Implementation
- [ ] Copy agent definitions to agents.yaml
- [ ] Test each agent's responses
- [ ] Verify tool access

## Task Configuration
- [ ] Copy task definitions to tasks.yaml
- [ ] Verify task dependencies
- [ ] Test task outputs

---

# Section 7: Validation

## Agent Testing
- [ ] YAML syntax valid
- [ ] Responses appropriate
- [ ] Tools accessible

## Task Validation
- [ ] Dependencies correct
- [ ] Outputs as expected

## Tool Verification
- [ ] APIs connected
- [ ] Functions working

## Environment Check
- [ ] Variables set
- [ ] Provider working

---

# Notes
- Keep YAML files up-to-date
- Test thoroughly before deployment
- Document custom tools
- Refer to [CrewAI Documentation](https://docs.crewai.com/) for best practices

