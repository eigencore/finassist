# Multi-Agent Architecture

## Overview

FinAssist employs a sophisticated multi-agent architecture designed to handle complex financial operations through specialized, coordinated agents. Each agent has a specific role and set of capabilities, working together to provide comprehensive financial analysis and management.

## Architecture Pattern

The system follows a **hierarchical multi-agent pattern** where:

- **Main Agent (Master Agent)**: Acts as the central orchestrator
- **Specialized Sub-Agents**: Handle specific domain tasks
- **Tool Integration**: Each agent has dedicated tools for their specialized functions
- **Event-Driven Communication**: Agents communicate through structured events and callbacks

## Agent Hierarchy

```
┌─────────────────────────────────────────┐
│            Main Agent                   │
│         (Master Agent)                  │
│                                         │
│  • Orchestrates operations              │
│  • Routes requests                      │
│  • Coordinates responses                │
└─────────────┬───────────────────────────┘
              │
              ├─── Parser Agent
              │    • Natural language processing
              │    • Transaction extraction
              │    • Context-aware parsing
              │
              └─── BigQuery Agent
                   • Database operations
                   • Data analysis
                   • SQL generation
```

## Agent Components

Each agent in the system follows a consistent structure:

### Core Components
- **Agent Implementation** (`agent.py`): Main agent logic and configuration
- **Tools & Functions** (`tools.py`): Specialized tools for the agent's domain
- **Prompts & Instructions** (`prompts.py`): LLM instructions and templates
- **Utilities** (`utils.py`): Helper functions and shared utilities

### Specialized Modules
Some agents include additional specialized modules for complex operations.

## Agent Catalog

### [Main Agent](main-agent/README.md)
**Role**: Central Orchestrator  
**Location**: `financial_assist/`

The master coordinator that:
- Receives user requests
- Determines appropriate sub-agents
- Manages overall system flow
- Aggregates responses

**Key Features**:
- Request routing logic
- Sub-agent coordination
- CRUD operations integration
- Multi-agent workflow management

---

### [Parser Agent](subagents/parser-agent/README.md)
**Role**: Natural Language Processing  
**Location**: `financial_assist/subagents/parser_agent/`

Specializes in converting natural language to structured financial data:
- Extracts transaction details from text
- Resolves temporal references ("yesterday", "last week")
- Maintains user context for improved accuracy
- Standardizes financial data format

**Key Features**:
- Context-aware parsing
- Dynamic instruction updates
- Temporal resolution
- User-specific context integration

---

### [BigQuery Agent](subagents/bigquery-agent/README.md)
**Role**: Database Operations & Analytics  
**Location**: `financial_assist/subagents/bigquery/`

Handles all database operations and analytical queries:
- Executes CRUD operations
- Generates SQL queries
- Performs financial analysis
- Manages data schemas

**Key Features**:
- BigQuery integration
- SQL generation and optimization
- Data validation
- Chase SQL module for complex operations

**Specialized Modules**:
- **Chase SQL**: Advanced SQL operations and query optimization

## Communication Patterns

### Agent-to-Agent Communication
```python
# Master Agent delegates to sub-agent
AgentTool(agent=call_parser_agent)

# Parser Agent retrieves context
user_context = get_user_context(user_id="user_001")

# BigQuery Agent executes operations
execute_crud_operation(transaction_data)
```

### Callback Mechanisms
Agents use callbacks for dynamic behavior:
- **Before Agent Callback**: Setup context and instructions
- **After Agent Callback**: Cleanup and result processing
- **Error Callbacks**: Handle failures gracefully

### Event-Driven Architecture
- Agents respond to specific events
- Asynchronous processing capabilities
- Scalable communication patterns

## Configuration Management

### Environment Variables
Each agent can be configured independently:
```bash
MASTER_MODEL=<model_for_main_agent>
PARSER_MODEL=<model_for_parser_agent>
BIGQUERY_MODEL=<model_for_bigquery_agent>
```

### Model Selection
- Different models for different agents
- Optimized for specific tasks
- Configurable temperature and parameters

## Data Flow

### Typical Request Flow
1. **User Input** → Main Agent
2. **Request Analysis** → Route to appropriate sub-agent
3. **Specialized Processing** → Sub-agent executes with tools
4. **Data Operations** → BigQuery Agent if needed
5. **Response Aggregation** → Main Agent coordinates
6. **User Response** → Structured output

### Context Propagation
- User context flows through agent hierarchy
- Temporal context (current date) automatically included
- Error context preserved across agent calls

## Design Principles

### Modularity
- Each agent has a single responsibility
- Clear separation of concerns
- Independent development and testing

### Extensibility
- Easy to add new agents
- Plugin-like architecture for tools
- Scalable communication patterns

### Reliability
- Error isolation between agents
- Graceful degradation
- Comprehensive error handling

### Performance
- Stateless agent design
- Efficient context management
- Optimized model selection

## Adding New Agents

To add a new agent to the system:

1. **Create Agent Directory**:
   ```bash
   mkdir -p financial_assist/subagents/new_agent
   ```

2. **Implement Core Components**:
   - `agent.py`: Agent configuration and logic
   - `tools.py`: Specialized tools
   - `prompts.py`: Instructions and templates

3. **Register with Main Agent**:
   ```python
   AgentTool(agent=new_agent)
   ```

4. **Document the Agent**:
   - Create documentation following the established pattern
   - Update this overview

## Performance Monitoring

### Metrics to Track
- Agent response times
- Tool execution performance  
- Context retrieval efficiency
- Error rates by agent

### Optimization Strategies
- Model selection optimization
- Context caching
- Tool performance tuning
- Communication pattern optimization

## Security Considerations

### Agent Isolation
- Each agent operates in controlled scope
- Limited cross-agent data access
- Secure context passing

### Input Validation
- Sanitized user inputs
- Template injection protection
- SQL injection prevention

### Access Control
- User-specific context access
- Database operation permissions
- Tool execution authorization

## Future Enhancements

### Planned Agents
- **Insight Agent**: Advanced financial analysis and pattern detection
- **Simulation Agent**: Financial scenario modeling
- **Ethics Agent**: Recommendation validation and safety
- **Report Agent**: Automated report generation

### Architecture Improvements
- Dynamic agent registration
- Load balancing for agent calls
- Advanced error recovery
- Real-time agent monitoring

## Troubleshooting

### Common Issues
- **Agent Not Responding**: Check model configuration and environment variables
- **Context Errors**: Verify user context retrieval and template escaping
- **Tool Failures**: Review tool permissions and dependencies
- **Communication Issues**: Check agent registration and callback setup

### Debug Mode
Enable detailed logging for agent operations:
```python
# Enable debug mode for agent interactions
agent.debug = True
```

For detailed information about each agent, refer to their individual documentation pages.