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

"""Type definitions for the financial assistant system."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    """Represents a financial transaction."""
    transaction_id: str = ""
    user_id: str = ""
    amount: str = ""
    currency: str = ""
    transaction_date: str = ""
    recorded_date: str = ""
    transaction_type: str = ""  # income or expense
    category: str = ""
    subcategory: str = ""
    establishment: str = ""
    notes: str = ""
    payment_method: str = ""

    def to_dict(self) -> dict:
        """Convert transaction to dictionary format."""
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "amount": self.amount,
            "currency": self.currency,
            "transaction_date": self.transaction_date,
            "recorded_date": self.recorded_date,
            "transaction_type": self.transaction_type,
            "category": self.category,
            "subcategory": self.subcategory,
            "establishment": self.establishment,
            "notes": self.notes,
            "payment_method": self.payment_method
        }

    def is_complete(self) -> bool:
        """Check if all required fields are filled."""
        required_fields = [
            self.amount, self.currency, self.transaction_date,
            self.transaction_type, self.category
        ]
        return all(field for field in required_fields)


@dataclass
class UserProfile:
    """Represents user profile information."""
    user_id: str = ""
    name: str = ""
    default_currency: str = "USD"
    preferred_categories: list = None
    
    def __post_init__(self):
        if self.preferred_categories is None:
            self.preferred_categories = []


@dataclass
class CategorySuggestion:
    """Represents a category suggestion from the categorization tool."""
    category: str
    subcategory: str
    confidence: float 