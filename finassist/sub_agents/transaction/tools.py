# Copyright 2025 Financial Assistant
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools specific to the transaction agent."""

import uuid
import re
from datetime import datetime, timedelta
from google.adk.tools import FunctionTool
from finassist.shared_libraries.types import Transaction


def extract_transaction_data(user_message: str) -> dict:
    """
    Intelligently extract transaction data from user's natural language message.
    
    Args:
        user_message: The user's message describing the transaction
        
    Returns:
        dict: Extracted transaction data
    """
    result = {}
    message_lower = user_message.lower()
    
    # Extract amount and currency
    amount_patterns = [
        r'\$(\d+(?:\.\d{2})?)\s*(?:usd|dollars?)?',  # $5 USD, $5, $5.00
        r'(\d+(?:\.\d{2})?)\s*(?:usd|dollars?)',     # 5 USD, 5 dollars
        r'(\d+(?:\.\d{2})?)\s*pesos?',               # 100 pesos
        r'€(\d+(?:\.\d{2})?)',                       # €50
        r'£(\d+(?:\.\d{2})?)',                       # £30
        r'(\d+(?:\.\d{2})?)\s*(?:euros?)',           # 50 euros
        r'(\d+(?:\.\d{2})?)\s*(?:pounds?)',          # 30 pounds
    ]
    
    for pattern in amount_patterns:
        match = re.search(pattern, message_lower)
        if match:
            result['amount'] = float(match.group(1))
            
            # Determine currency based on pattern
            if '$' in pattern or 'usd' in message_lower or 'dollar' in message_lower:
                result['currency'] = 'USD'
            elif 'peso' in message_lower:
                result['currency'] = 'MXN'
            elif '€' in pattern or 'euro' in message_lower:
                result['currency'] = 'EUR'
            elif '£' in pattern or 'pound' in message_lower:
                result['currency'] = 'GBP'
            break
    
    # Extract establishment/merchant
    establishments = {
        'netflix': 'Netflix',
        'spotify': 'Spotify',
        'gym': 'Gym',
        'amazon': 'Amazon',
        'starbucks': 'Starbucks',
        'uber': 'Uber',
        'mcdonalds': 'McDonald\'s',
    }
    
    for keyword, name in establishments.items():
        if keyword in message_lower:
            result['establishment'] = name
            break
    
    # Extract payment method
    if any(term in message_lower for term in ['credit card', 'credit']):
        result['payment_method'] = 'Credit Card'
    elif any(term in message_lower for term in ['debit card', 'debit']):
        result['payment_method'] = 'Debit Card'
    elif 'cash' in message_lower:
        result['payment_method'] = 'Cash'
    elif any(term in message_lower for term in ['bank transfer', 'transfer']):
        result['payment_method'] = 'Bank Transfer'
    
    # Extract transaction type
    if any(term in message_lower for term in ['paid', 'spent', 'bought', 'purchased']):
        result['transaction_type'] = 'expense'
    elif any(term in message_lower for term in ['received', 'earned', 'got']):
        result['transaction_type'] = 'income'
    
    # Extract date
    if 'today' in message_lower:
        result['transaction_date'] = datetime.now().strftime('%Y-%m-%d')
    elif 'yesterday' in message_lower:
        result['transaction_date'] = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    return result


def generate_transaction_id() -> str:
    """
    Generate a unique transaction ID.
    
    Returns:
        str: Unique transaction identifier
    """
    return f"TXN_{uuid.uuid4().hex[:8].upper()}"


def get_current_timestamp() -> str:
    """
    Get the current timestamp for recorded_date.
    
    Returns:
        str: Current timestamp in ISO format
    """
    return datetime.now().isoformat()


def format_transaction_summary(transaction_data: dict) -> str:
    """
    Format transaction data for user confirmation.
    
    Args:
        transaction_data: Dictionary containing transaction information
        
    Returns:
        str: Formatted summary for user review
    """
    summary = "📋 TRANSACTION SUMMARY:\n"
    summary += "=" * 30 + "\n"
    summary += f"💰 Amount: {transaction_data.get('amount', 'N/A')} {transaction_data.get('currency', 'N/A')}\n"
    summary += f"🏪 Establishment: {transaction_data.get('establishment', 'N/A')}\n"
    summary += f"📅 Date: {transaction_data.get('transaction_date', 'N/A')}\n"
    summary += f"📂 Category: {transaction_data.get('category', 'N/A')} > {transaction_data.get('subcategory', 'N/A')}\n"
    summary += f"💳 Payment Method: {transaction_data.get('payment_method', 'N/A')}\n"
    summary += f"📝 Type: {transaction_data.get('transaction_type', 'N/A')}\n"
    
    if transaction_data.get('notes'):
        summary += f"📌 Notes: {transaction_data.get('notes')}\n"
    
    summary += "=" * 30 + "\n"
    summary += "Is this information correct? Would you like to make any changes?"
    
    return summary


def validate_transaction_completeness(transaction_data: dict) -> tuple[bool, list[str]]:
    """
    Check if transaction has all required fields completed.
    
    Args:
        transaction_data: Dictionary containing transaction information
        
    Returns:
        tuple: (is_complete, list_of_missing_fields)
    """
    required_fields = {
        'amount': 'Amount',
        'currency': 'Currency',
        'transaction_date': 'Transaction Date',
        'transaction_type': 'Transaction Type',
        'category': 'Category'
    }
    
    missing_fields = []
    for field, display_name in required_fields.items():
        if not transaction_data.get(field):
            missing_fields.append(display_name)
    
    return len(missing_fields) == 0, missing_fields


# Create tools
extract_transaction_data_tool = FunctionTool(func=extract_transaction_data)

generate_transaction_id_tool = FunctionTool(func=generate_transaction_id)

get_current_timestamp_tool = FunctionTool(func=get_current_timestamp)

format_transaction_summary_tool = FunctionTool(func=format_transaction_summary)

validate_transaction_completeness_tool = FunctionTool(func=validate_transaction_completeness) 