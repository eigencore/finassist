#!/usr/bin/env python3
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

"""Demo script for the Financial Assistant multi-agent system."""

from finassist.agent import root_agent
from finassist.shared_libraries.types import UserProfile


def demo_transaction_recording():
    """Demo transaction recording functionality."""
    print("=" * 60)
    print("DEMO: Transaction Recording")
    print("=" * 60)
    
    # Create a sample user profile
    user_profile = UserProfile(
        user_id="demo_user",
        name="Demo User",
        default_currency="USD",
        preferred_categories=["Food", "Entertainment", "Transportation"]
    )
    
    # Example transaction messages
    test_messages = [
        "I spent 100 pesos on Netflix today with my BBVA credit card",
        "I bought groceries for $50 at Walmart yesterday",
        "I received my salary of $3000 today"
    ]
    
    for message in test_messages:
        print(f"\nUser: {message}")
        print("-" * 40)
        
        # In a real implementation, you would call:
        # response = root_agent.generate_content(message, user_profile=user_profile)
        # print(f"Assistant: {response}")
        
        print("Assistant: [Would route to transaction_agent and process the transaction]")


def demo_consulting():
    """Demo consulting functionality."""
    print("\n" + "=" * 60)
    print("DEMO: Financial Consulting")
    print("=" * 60)
    
    # Example consulting questions
    test_questions = [
        "What is the stock market?",
        "How does compound interest work?",
        "What's the difference between a 401k and IRA?"
    ]
    
    for question in test_questions:
        print(f"\nUser: {question}")
        print("-" * 40)
        
        # In a real implementation, you would call:
        # response = root_agent.generate_content(question)
        # print(f"Assistant: {response}")
        
        print("Assistant: [Would route to consulting_agent and provide educational response]")


def main():
    """Run the demo."""
    print("Financial Assistant Multi-Agent System Demo")
    print("This demo shows how the system would work with real ADK integration")
    
    demo_transaction_recording()
    demo_consulting()
    
    print("\n" + "=" * 60)
    print("Demo completed! The system is ready for integration with ADK.")
    print("=" * 60)


if __name__ == "__main__":
    main() 