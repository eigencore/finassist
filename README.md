# Financial Assistant Multi-Agent System

A sophisticated multi-agent system built with Google's Agent Development Kit (ADK) for managing financial transactions through natural conversation and providing educational financial guidance.

## System Architecture

### Root Agent (Orchestrator)
- **Function**: Identifies user intent and routes to specialized agents
- **Responsibilities**:
  - Classify whether user wants to record a transaction or make financial queries
  - Direct to `transaction_agent` or `consulting_agent` accordingly
  - Maintain conversation context

### Transaction Agent
- **Function**: Process and complete financial transaction information
- **Objective**: Fill complete transaction JSON through natural conversation
- **Capabilities**:
  - Extract information from user's initial prompt
  - Ask specific questions to complete missing fields
  - Validate information before finalizing
  - Automatic categorization using LLM
  - Confirm with user before processing

### Consulting Agent
- **Function**: Answer educational queries about personal finance
- **Capabilities**:
  - Explain financial concepts in simple terms
  - Provide practical examples and actionable advice
  - Cover topics like investments, taxes, budgeting, etc.
  - Educational, clear, and accessible responses

## Transaction Data Structure

The system collects complete transaction information:

```json
{
  "transaction_id": "",
  "user_id": "",
  "amount": "",
  "currency": "",
  "transaction_date": "",
  "recorded_date": "",
  "transaction_type": "",
  "category": "",
  "subcategory": "",
  "establishment": "",
  "notes": "",
  "payment_method": ""
}
```

## Key Features

### Automatic Categorization
- Uses LLM-powered categorization tool
- Considers establishment, description, amount, and context
- Predefined categories: Food, Transportation, Entertainment, Services, Shopping, Health, Education, Housing, Income
- Each category has detailed subcategories

### Validation Tools
- Currency validation (supports 15+ currencies)
- Amount validation (positive numbers only)
- Date format validation (multiple formats supported)
- Payment method validation

### Natural Conversation Flow
- Extracts available information from initial message
- Asks focused questions for missing data
- Provides clear confirmations
- Handles corrections gracefully

## Example Interactions

### Transaction Recording
```
User: "Today I spent 100 pesos on my Netflix subscription and paid with my BBVA credit card"

Root Agent: [Routes to transaction_agent]

Transaction Agent: "I understand you spent 100 pesos on Netflix with your BBVA card. I've automatically categorized this as 'Entertainment > Streaming'. Could you confirm the exact date of this transaction?"

User: "It was today, June 1st"

Transaction Agent: "Perfect. Processing transaction:
- Amount: 100 pesos
- Establishment: Netflix  
- Date: June 1st, 2025
- Category: Entertainment > Streaming
- Payment method: BBVA card
- Type: Expense

Is this correct? Would you like to add any additional notes?"

User: "Yes, that's correct"

Transaction Agent: [Executes save_transaction() which prints the data]
```

### Educational Consulting
```
User: "What is compound interest?"

Root Agent: [Routes to consulting_agent]

Consulting Agent: "Compound interest is the interest earned on both the initial principal and the accumulated interest from previous periods. It's often called 'interest on interest' and is a powerful concept in finance..."
```

## File Structure

```
finassist/
├── agent.py                    # Root agent (orchestrator)
├── __init__.py
├── prompt.py                   # Root agent prompts
├── demo.py                     # Demo script
├── README.md                   # This file
├── profiles/
│   └── transaction_template.json
├── shared_libraries/
│   ├── constants.py           # Categories, currencies, etc.
│   ├── __init__.py
│   └── types.py              # Data structures
├── sub_agents/
│   ├── __init__.py
│   ├── transaction/
│   │   ├── agent.py          # Transaction agent
│   │   ├── __init__.py
│   │   ├── prompt.py         # Transaction prompts
│   │   └── tools.py          # Transaction-specific tools
│   └── consulting/
│       ├── agent.py          # Consulting agent
│       ├── __init__.py
│       └── prompt.py         # Consulting prompts
└── tools/
    ├── __init__.py
    ├── categorization.py     # LLM categorization tool
    └── validation.py         # Validation tools
```

## Available Tools

### Transaction Agent Tools
- `categorize_transaction`: Automatic LLM-based categorization
- `validate_currency`: Currency code validation
- `validate_amount`: Amount validation
- `validate_date`: Date format validation
- `validate_payment_method`: Payment method validation
- `generate_transaction_id`: Unique ID generation
- `get_current_timestamp`: Timestamp generation
- `format_transaction_summary`: User-friendly summary
- `validate_transaction_completeness`: Completeness check
- `save_transaction`: Data persistence (simulated)

### Consulting Agent Tools
- No specific tools (uses knowledge-based responses)

## Usage

### Basic Usage
```python
from finassist.agent import root_agent
from finassist.shared_libraries.types import UserProfile

# Create user profile
user_profile = UserProfile(
    user_id="user123",
    name="John Doe",
    default_currency="USD"
)

# Process user message
response = root_agent.generate_content(
    "I spent $50 on groceries today",
    user_profile=user_profile
)
```

### Running the Demo
```bash
python finassist/demo.py
```

## Supported Categories

- **Food**: Restaurants, Groceries, Fast Food, Coffee/Tea, Delivery, Alcohol, Snacks
- **Transportation**: Gas, Public Transport, Taxi/Uber, Parking, Car Maintenance, Tolls, Flights, Car Rental
- **Entertainment**: Movies, Streaming, Games, Books, Music, Sports Events, Concerts, Hobbies
- **Services**: Utilities, Internet, Phone, Insurance, Bank Fees, Subscriptions, Professional Services
- **Shopping**: Clothing, Electronics, Home Items, Gifts, Personal Care, Accessories, Online Shopping
- **Health**: Medical, Pharmacy, Dental, Vision, Fitness, Mental Health, Supplements
- **Education**: Tuition, Books, Courses, Training, Certifications, Online Learning
- **Housing**: Rent, Mortgage, Home Improvement, Furniture, Appliances, Cleaning, Gardening
- **Income**: Salary, Freelance, Investment, Bonus, Rental, Business, Other Income

## Supported Currencies

USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, MXN, BRL, ARS, CLP, COP, PEN, UYU

## Technical Requirements

- Google Agent Development Kit (ADK)
- Python 3.8+
- Access to Gemini 2.0 Flash model

## License

Licensed under the Apache License, Version 2.0