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

"""Constants for the financial assistant system."""

# Transaction Types
TRANSACTION_TYPES = ["income", "expense"]

# Main Categories and their subcategories
CATEGORIES = {
    "Food": [
        "Restaurants", "Groceries", "Fast Food", "Coffee/Tea", 
        "Delivery", "Alcohol", "Snacks"
    ],
    "Transportation": [
        "Gas", "Public Transport", "Taxi/Uber", "Parking", 
        "Car Maintenance", "Tolls", "Flights", "Car Rental"
    ],
    "Entertainment": [
        "Movies", "Streaming", "Games", "Books", "Music", 
        "Sports Events", "Concerts", "Hobbies"
    ],
    "Services": [
        "Utilities", "Internet", "Phone", "Insurance", 
        "Bank Fees", "Subscriptions", "Professional Services"
    ],
    "Shopping": [
        "Clothing", "Electronics", "Home Items", "Gifts", 
        "Personal Care", "Accessories", "Online Shopping"
    ],
    "Health": [
        "Medical", "Pharmacy", "Dental", "Vision", 
        "Fitness", "Mental Health", "Supplements"
    ],
    "Education": [
        "Tuition", "Books", "Courses", "Training", 
        "Certifications", "Online Learning"
    ],
    "Housing": [
        "Rent", "Mortgage", "Home Improvement", "Furniture", 
        "Appliances", "Cleaning", "Gardening"
    ],
    "Income": [
        "Salary", "Freelance", "Investment", "Bonus", 
        "Rental", "Business", "Other Income"
    ]
}

# Supported Currencies
SUPPORTED_CURRENCIES = [
    "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY",
    "MXN", "BRL", "ARS", "CLP", "COP", "PEN", "UYU"
]

# Payment Methods
PAYMENT_METHODS = [
    "Credit Card", "Debit Card", "Cash", "Bank Transfer", 
    "PayPal", "Apple Pay", "Google Pay", "Venmo", "Zelle", "Other"
] 