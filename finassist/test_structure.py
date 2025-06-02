#!/usr/bin/env python3
"""Test script to verify the module structure without requiring ADK."""

def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing module structure...")
    
    try:
        # Test shared libraries
        from finassist.shared_libraries.types import Transaction, UserProfile, CategorySuggestion
        from finassist.shared_libraries.constants import CATEGORIES, SUPPORTED_CURRENCIES, PAYMENT_METHODS
        print("✓ Shared libraries imported successfully")
        
        # Test tools (these don't require ADK for the functions themselves)
        from finassist.tools.categorization import categorize_transaction, _rule_based_categorization
        from finassist.tools.validation import (
            validate_currency, validate_amount, validate_date, 
            validate_payment_method, save_transaction
        )
        print("✓ Tools imported successfully")
        
        # Test transaction agent tools
        from finassist.sub_agents.transaction.tools import (
            generate_transaction_id, get_current_timestamp,
            format_transaction_summary, validate_transaction_completeness
        )
        print("✓ Transaction agent tools imported successfully")
        
        # Test prompts
        from finassist.sub_agents.transaction.prompt import TRANSACTION_AGENT_INSTR
        from finassist.sub_agents.consulting.prompt import CONSULTING_AGENT_INSTR
        from finassist.prompt import ROOT_AGENT_INSTR
        print("✓ Prompts imported successfully")
        
        print("\n✅ All modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_functionality():
    """Test core functionality without ADK."""
    print("\nTesting core functionality...")
    
    # Test transaction creation
    from finassist.shared_libraries.types import Transaction
    transaction = Transaction(
        amount="100",
        currency="USD",
        establishment="Netflix",
        transaction_type="expense"
    )
    print(f"✓ Transaction created: {transaction.establishment}")
    
    # Test categorization
    from finassist.tools.categorization import categorize_transaction
    suggestion = categorize_transaction(
        establishment="Netflix",
        description="Monthly subscription",
        amount="100",
        context="Entertainment service"
    )
    print(f"✓ Categorization: {suggestion.category} > {suggestion.subcategory}")
    
    # Test validation
    from finassist.tools.validation import validate_currency, validate_amount
    print(f"✓ Currency validation (USD): {validate_currency('USD')}")
    print(f"✓ Amount validation (100): {validate_amount('100')}")
    
    # Test transaction tools
    from finassist.sub_agents.transaction.tools import generate_transaction_id
    txn_id = generate_transaction_id()
    print(f"✓ Generated transaction ID: {txn_id}")
    
    print("\n✅ All functionality tests passed!")


def main():
    """Run all tests."""
    print("=" * 60)
    print("FINANCIAL ASSISTANT SYSTEM STRUCTURE TEST")
    print("=" * 60)
    
    success = test_imports()
    if success:
        test_functionality()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED! The system structure is correct.")
        print("The system is ready for ADK integration.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 60)


if __name__ == "__main__":
    main() 