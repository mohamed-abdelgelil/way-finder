# Tech Stack

## Language & Runtime
- Python 3.11+
- Jupyter Notebook (`egypt_travel_agent.ipynb`) as the primary entry point

## Key Libraries
- **[Strands Agents SDK](https://github.com/strands-agents/sdk-python)** (`strands-agents`, `strands-agents-tools`) — agent framework and `@tool` decorator
- **Amazon Bedrock** (`strands.models.bedrock.BedrockModel`) — LLM provider
- **Claude Sonnet** (`us.anthropic.claude-sonnet-4-20250514`) — model used by the agent
- **unittest** (stdlib) — test framework

## AWS Requirements
- Valid AWS credentials required (env vars or `aws configure`)
- Bedrock access enabled in `us-east-1`

## Installation

```bash
pip install strands-agents strands-agents-tools
```

## Common Commands

### Run tests
```bash
python -m unittest test_integration.py
```

### Launch the notebook
```bash
jupyter notebook egypt_travel_agent.ipynb
```

## Tool Decorator Pattern
All tool functions use the `@tool` decorator from `strands`. In tests, `strands` is mocked so the decorator becomes a pass-through — tool functions remain plain callables.
