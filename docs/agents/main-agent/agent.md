# Main Agent (Master Agent)

## Overview

The Main Agent, also known as the Master Agent, is the central orchestrator of the FinAssist system. It coordinates financial operations by managing communication between specialized sub-agents and database operations.

## File Location
```
financial_assist/agent.py
```

## Architecture

The Main Agent follows a hierarchical multi-agent architecture where it acts as the root coordinator, delegating specific tasks to specialized sub-agents while maintaining overall system control.

## Agent Configuration

### Basic Setup
```python
master_agent = LlmAgent(
    name="master_agent",
    model=LiteLlm(MODEL),
    description="A master agent that orchestrates financial operations by coordinating parser and database agents.",
    instruction=master_agent_instruction(),
    tools=[
        AgentTool(agent=call_parser_agent),
        execute_crud_operation,
    ]
)
```

### Model Configuration
- **Model**: Uses `LiteLlm` with a configurable model specified by the `MASTER_MODEL` environment variable
- **Name**: `master_agent`
- **Alias**: Also available as `root_agent`

## Dependencies

### External Libraries
- `google.adk.agents.LlmAgent`: Core agent framework
- `google.adk.models.lite_llm.LiteLlm`: Language model interface
- `google.adk.tools.agent_tool.AgentTool`: Tool for agent delegation
- `google.genai.types`: Google GenAI type definitions

### Internal Modules
- `prompts.master_agent_instruction`: Contains the agent's system instructions
- `subagents.parser_agent.agent.parser_agent`: Parser sub-agent for text processing
- `tools.crud_service_tool`: Database operations tool

## Available Tools

### 1. Parser Agent Tool
- **Purpose**: Delegates text parsing and natural language processing tasks
- **Implementation**: `AgentTool(agent=call_parser_agent)`
- **Use Case**: Processing user input like "yesterday I paid Netflix"

### 2. CRUD Service Tool
- **Purpose**: Executes database operations (Create, Read, Update, Delete)
- **Implementation**: `execute_crud_operation`
- **Use Case**: Managing financial transaction data

## Key Features

### Orchestration Capabilities
- **Task Distribution**: Routes different types of requests to appropriate sub-agents
- **Coordination**: Manages the flow of information between parser and database agents
- **Decision Making**: Determines which tools to use based on user input and context

### Integration Points
- **Parser Integration**: Seamlessly communicates with the parser agent for text processing
- **Database Integration**: Direct access to CRUD operations for data management
- **Extensible Design**: Can easily incorporate additional tools and sub-agents

## Environment Variables

### Required Configuration
```bash
MASTER_MODEL=<model_name>
```

**Description**: Specifies which language model the master agent should use. This allows for flexible model selection without code changes.

## Usage Examples

### Basic Agent Initialization
```python
from financial_assist.agent import master_agent, root_agent

# Both references point to the same agent instance
agent = master_agent
# or
agent = root_agent
```

### Agent Execution Context
The master agent is designed to:
1. Receive user requests for financial operations
2. Analyze the request type and complexity
3. Delegate to appropriate sub-agents when needed
4. Execute database operations directly when appropriate
5. Coordinate responses from multiple tools
6. Return coherent results to the user

## Design Patterns

### Command Pattern
The agent uses a command pattern where different types of financial operations are encapsulated as tools that can be executed based on the user's intent.

### Delegation Pattern
Complex tasks are broken down and delegated to specialized sub-agents, allowing for modular and maintainable code.

### Chain of Responsibility
The agent can process requests through a chain of tools and sub-agents until the appropriate handler is found.

## Performance Considerations

- **Lazy Loading**: Sub-agents are imported and initialized only when needed
- **Stateless Design**: The agent doesn't maintain state between requests, ensuring scalability
- **Efficient Routing**: Quick decision-making process to determine the appropriate tool or sub-agent

## Error Handling

The master agent is designed to handle various error scenarios:
- Missing environment variables
- Sub-agent failures
- Database connectivity issues
- Invalid user inputs

## Future Extensions

The current architecture allows for easy extension with additional:
- Sub-agents for specialized financial analysis
- Tools for external API integrations
- Enhanced coordination mechanisms
- Advanced error recovery strategies