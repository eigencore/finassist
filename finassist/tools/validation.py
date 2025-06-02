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

"""Validation tools for transaction data."""

import re
from datetime import datetime
from google.adk.tools import FunctionTool
from finassist.shared_libraries.constants import SUPPORTED_CURRENCIES, PAYMENT_METHODS


def validate_currency(currency: str) -> bool:
    """
    Validate if the currency is supported.
    
    Args:
        currency: Currency code to validate
        
    Returns:
        bool: True if currency is valid, False otherwise
    """
    currency_upper = currency.upper()
    return currency_upper in SUPPORTED_CURRENCIES


def validate_amount(amount: str) -> bool:
    """
    Validate if the amount is a positive number.
    
    Args:
        amount: Amount string to validate
        
    Returns:
        bool: True if amount is valid, False otherwise
    """
    try:
        amount_float = float(amount.replace(',', ''))
        return amount_float > 0
    except (ValueError, AttributeError):
        return False


def validate_date(date_string: str) -> bool:
    """
    Validate if the date string is in a valid format.
    
    Args:
        date_string: Date string to validate
        
    Returns:
        bool: True if date is valid, False otherwise
    """
    date_formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%Y-%m-%d %H:%M:%S"
    ]
    
    for date_format in date_formats:
        try:
            datetime.strptime(date_string, date_format)
            return True
        except ValueError:
            continue
    
    return False


def validate_payment_method(payment_method: str) -> bool:
    """
    Validate if the payment method is recognized.
    
    Args:
        payment_method: Payment method to validate
        
    Returns:
        bool: True if payment method is valid, False otherwise
    """
    # Check if it's in our predefined list or if it contains card-related keywords
    if any(method.lower() in payment_method.lower() for method in PAYMENT_METHODS):
        return True
    
    # Check for card-related keywords
    card_keywords = ['card', 'credit', 'debit', 'visa', 'mastercard', 'amex', 'discover']
    if any(keyword in payment_method.lower() for keyword in card_keywords):
        return True
    
    return False


def save_transaction(transaction_data: dict) -> str:
    """
    Simulate saving transaction data by printing it.
    
    Args:
        transaction_data: Dictionary containing transaction information
        
    Returns:
        str: Confirmation message
    """
    print("=" * 50)
    print("TRANSACTION SAVED SUCCESSFULLY")
    print("=" * 50)
    for key, value in transaction_data.items():
        print(f"{key}: {value}")
    print("=" * 50)
    
    return "Transaction has been successfully recorded in the system."


# Create tools
validate_currency_tool = FunctionTool(func=validate_currency)

validate_amount_tool = FunctionTool(func=validate_amount)

validate_date_tool = FunctionTool(func=validate_date)

validate_payment_method_tool = FunctionTool(func=validate_payment_method)

save_transaction_tool = FunctionTool(func=save_transaction) 