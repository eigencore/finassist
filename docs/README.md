# FinAssist

FinAssist is an autonomous multi-agent financial auditor system designed for personal and small business financial management. Unlike traditional financial tools, FinAssist not only organizes transactions but also detects critical patterns, simulates future scenarios, and delivers personalized recommendations through natural language processing.

## Current Status

### ✅ What's Working:
- **Multi-agent architecture** implemented using Google Agent Development Kit (ADK)
- **Natural language transaction processing** - users can say "I paid Netflix $5 with my debit card today"
- **TransactionAgent (Parser)** successfully extracts structured data from user requests
- **DatabaseOpsAgent (CRUD Master)** handles database operations
- **CREATE operations** for transactions fully functional with BigQuery integration

### ⚠️ Known Issues:
- **Account creation fails** due to `due_date` field formatting problems
- **Account balances don't update automatically** when transactions are recorded
- **Missing CRUD operations**: READ, UPDATE, and DELETE not yet implemented

### 🔧 In Development:
- Complete CRUD operations implementation
- Automatic balance updates for linked accounts
- CategorizerAgent for intelligent transaction classification

## Current Architecture

![FinAssist Architecture](../static/crud_system.png)

The system follows a multi-agent workflow:
1. **User** submits financial requests in natural language
2. **TransactionAgent** parses and structures the financial data
3. **DatabaseOpsAgent** executes database operations using a deterministic CRUD tool
4. **BigQuery** stores transaction and account data
5. **User** receives confirmation and feedback

## Key Features Implemented

- **Natural Language Processing**: "Paid my Netflix subscription $15 today" → Structured transaction data
- **Deterministic CRUD Operations**: Direct database operations without LLM SQL generation
- **Security**: All operations include `user_id` validation for data isolation
- **Automatic ID Generation**: UUID generation for transactions and accounts
- **Multi-currency Support**: Built-in support for different currencies

## Tech Stack

- **Agent Framework**: Google Agent Development Kit (ADK)
- **Database**: Google BigQuery
- **Language Models**: Configurable LLM support through LiteLLM
- **Cloud Platform**: Google Cloud Functions & Pub/Sub for agent communication
- **Authentication**: Firebase Auth (planned)

## Next Steps

1. **Complete CRUD Operations** - Implement READ, UPDATE, DELETE functionality
2. **Smart Balance Updates** - When you pay with debit card, account balance automatically decreases
3. **Account Management** - Fix account creation and enable multiple account management
4. **Intelligent Categorization** - Implement CategorizerAgent for automatic expense categorization
5. **Advanced Analytics** - Add InsightAgent for spending pattern analysis

## Project Structure

```
financial_assist/
├── agents/                 # Multi-agent system
│   ├── transaction_agent/  # Natural language parser
│   └── database_ops_agent/ # CRUD operations manager
├── tools/                  # Direct database tools
│   └── crud_tools.py      # Deterministic database operations
├── utils/                  # Utilities and helpers
└── services/              # Business logic services
```

## Getting Started

[Installation and setup instructions would go here]

## Contributing

This project is under active development. Current priorities:
- Completing CRUD operations
- Implementing automatic balance updates
- Adding comprehensive error handling and validation
