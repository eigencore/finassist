# Parser Agent

## Overview

The Parser Agent is a specialized sub-agent within the FinAssist system responsible for parsing financial information from natural language input into structured data. It transforms user queries like "yesterday I paid Netflix $15" into standardized financial transaction records.

## File Location
```
financial_assist/subagents/parser_agent/agent.py
```

## Architecture

The Parser Agent operates as a context-aware language processing unit that:
- Receives natural language financial descriptions
- Extracts structured financial data
- Maintains user context for improved parsing accuracy
- Provides consistent data formatting for downstream processing

## Agent Configuration

### Basic Setup
```python
parser_agent = LlmAgent(
    name="call_parser_agent",
    model=LiteLlm(MODEL),
    description="A specialized agent that parses financial information from natural language into structured data.",
    instruction=parser_agent_instruction(),
    tools=[],
    before_agent_callback=setup_before_agent_call,
    include_contents='default',
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5,
    )
)
```

### Model Configuration
- **Model**: Uses `LiteLlm` with model specified by `PARSER_MODEL` environment variable
- **Name**: `call_parser_agent`
- **Temperature**: 0.5 (balanced between creativity and consistency)
- **Tools**: None (specialized for parsing only)

## Dependencies

### External Libraries
- `google.adk.agents.LlmAgent`: Core agent framework
- `google.adk.models.lite_llm.LiteLlm`: Language model interface
- `google.adk.agents.callback_context.CallbackContext`: Context management
- `google.genai.types`: Google GenAI type definitions

### Internal Modules
- `prompts.parser_agent_instruction`: Contains the agent's parsing instructions
- `financial_assist.subagents.bigquery.tools.get_user_context`: User context retrieval

### Standard Libraries
- `os`: Environment variable access
- `datetime`: Date/time operations
- `json`: JSON data handling

## Key Features

### Dynamic Context Management

#### Pre-Execution Setup
```python
def setup_before_agent_call(callback_context: CallbackContext):
    """Setup the agent with updated context before each call."""
    
    user_context = get_user_context(user_id="user_001") # hardcoded for user ID
    user_context = user_context.replace('{', '{{').replace('}', '}}')
    
    callback_context._invocation_context.agent.instruction = (
        parser_agent_instruction()
        + f"""
--------- The User Context ---------
{user_context}

current_date: {current_date}
"""
    )
```

#### Context Features
- **User Context Injection**: Retrieves and injects user-specific financial context before each parsing operation
- **Current Date Awareness**: Automatically includes current date for relative time parsing
- **Template Safety**: Escapes curly braces to prevent template injection issues

### Natural Language Processing
- **Financial Entity Recognition**: Identifies amounts, dates, merchants, and categories
- **Temporal Resolution**: Converts relative dates ("yesterday", "last week") to absolute dates
- **Transaction Classification**: Determines transaction types (expense, income, transfer)

### Data Standardization
- **Consistent Output Format**: Produces uniform structured data regardless of input variation
- **Validation**: Ensures extracted data meets required financial data standards
- **Error Handling**: Manages ambiguous or incomplete input gracefully

## Environment Variables

### Required Configuration
```bash
PARSER_MODEL=<model_name>
```

**Description**: Specifies which language model the parser agent should use for natural language processing tasks.

## Context Management

### User Context Integration
The agent retrieves user-specific context to improve parsing accuracy:
- **User ID**: Currently hardcoded as "user_001"
- **Financial History**: Previous transactions and patterns
- **User Preferences**: Customized categories and merchant mappings
- **Account Information**: Available accounts and balances

### Current Date Context
```python
current_date = datetime.datetime.now().strftime("%Y-%m-%d")
```
- **Format**: YYYY-MM-DD
- **Usage**: Resolves relative date references in user input
- **Updates**: Refreshed on each module import

## Callback Mechanism

### Before Agent Callback
The `setup_before_agent_call` function ensures:
1. **Fresh Context**: User context is retrieved before each parsing operation
2. **Updated Instructions**: Agent instructions include current user state
3. **Date Awareness**: Current date is always available for temporal parsing
4. **Security**: Template strings are properly escaped

### Execution Flow
1. User submits natural language financial input
2. `setup_before_agent_call` executes
3. User context is retrieved from BigQuery
4. Current date is added to context
5. Agent instructions are dynamically updated
6. Parser agent processes the input with full context
7. Structured financial data is returned

## Usage Examples

### Typical Input Patterns
- "I spent $25 on lunch at McDonald's yesterday"
- "Received salary payment of $3000 last Friday"
- "Netflix subscription $15.99 charged to my credit card"
- "Cash withdrawal $100 from ATM"

### Expected Output Structure
The parser agent transforms these inputs into structured data containing:
- **Amount**: Numerical value
- **Date**: Resolved absolute date
- **Merchant/Description**: Standardized merchant name
- **Category**: Auto-assigned category
- **Account**: Identified account
- **Transaction Type**: Income/Expense/Transfer

## Performance Considerations

### Efficiency Features
- **Stateless Design**: No persistent state between calls
- **Context Caching**: User context retrieved efficiently from BigQuery
- **Temperature Optimization**: 0.5 temperature balances accuracy and speed
- **No External Tools**: Minimizes latency by avoiding tool calls

### Scalability
- **User ID Parameterization**: Ready for multi-user scenarios
- **Modular Design**: Easy to extend with additional parsing capabilities
- **Memory Efficient**: Dynamic context loading prevents memory bloat

## Current Limitations

### Hardcoded Elements
- **User ID**: Currently hardcoded as "user_001"
- **Single User**: Not yet optimized for multi-user scenarios

### Template Escaping
- **Manual Escaping**: Context strings manually escaped for template safety
- **Potential Issues**: Complex user data might need additional escaping

## Future Enhancements

### Multi-User Support
- Dynamic user ID resolution
- User-specific model fine-tuning
- Personalized parsing rules

### Advanced Parsing
- Multi-language support
- Receipt image parsing integration
- Bank statement parsing
- Investment transaction parsing

### Performance Optimization
- Context caching mechanisms
- Batch processing capabilities
- Real-time parsing validation

## Error Handling

The parser agent handles various error scenarios:
- **Invalid Date References**: Graceful handling of unparseable dates
- **Missing Context**: Fallback behavior when user context unavailable
- **Malformed Input**: Robust parsing of incomplete information
- **Model Failures**: Appropriate error responses for LLM issues