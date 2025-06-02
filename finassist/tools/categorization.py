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

"""Categorization tools for automatic transaction classification."""

import json
from google.adk.tools import FunctionTool
from finassist.shared_libraries.constants import CATEGORIES
from finassist.shared_libraries.types import CategorySuggestion


def categorize_transaction(
    establishment: str = "",
    description: str = "",
    amount: str = "",
    context: str = ""
) -> CategorySuggestion:
    """
    Automatically categorize a transaction using LLM analysis.
    
    Args:
        establishment: The establishment or merchant name
        description: Additional transaction description
        amount: Transaction amount (for context)
        context: Additional context about the transaction
        
    Returns:
        CategorySuggestion with category, subcategory, and confidence
    """
    # Build the context for categorization
    transaction_info = f"""
    Establishment: {establishment}
    Description: {description}
    Amount: {amount}
    Context: {context}
    """
    
    # Available categories for reference
    categories_text = ""
    for category, subcategories in CATEGORIES.items():
        categories_text += f"{category}: {', '.join(subcategories)}\n"
    
    # For demonstration, we'll use rule-based logic 
    # In a real implementation, this would call an LLM
    category, subcategory = _rule_based_categorization(establishment, description)
    
    return CategorySuggestion(
        category=category,
        subcategory=subcategory,
        confidence=0.85
    )


def _rule_based_categorization(establishment: str, description: str) -> tuple[str, str]:
    """Simple rule-based categorization for demonstration."""
    establishment_lower = establishment.lower()
    description_lower = description.lower()
    
    # Entertainment services
    if any(keyword in establishment_lower for keyword in ['netflix', 'spotify', 'hulu', 'disney', 'prime']):
        return "Entertainment", "Streaming"
    
    # Food establishments
    if any(keyword in establishment_lower for keyword in ['starbucks', 'mcdonalds', 'restaurant', 'cafe']):
        return "Food", "Restaurants"
    
    # Transportation
    if any(keyword in establishment_lower for keyword in ['gas', 'shell', 'exxon', 'uber', 'lyft']):
        return "Transportation", "Gas" if 'gas' in establishment_lower else "Taxi/Uber"
    
    # Shopping
    if any(keyword in establishment_lower for keyword in ['amazon', 'walmart', 'target', 'mall']):
        return "Shopping", "Online Shopping" if 'amazon' in establishment_lower else "General"
    
    # Default categorization
    return "Services", "Other"


categorize_transaction_tool = FunctionTool(func=categorize_transaction) 