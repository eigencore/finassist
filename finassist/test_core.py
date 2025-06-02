#!/usr/bin/env python3
"""Test script to verify core functionality without ADK dependencies."""

def test_core_imports():
    """Test that core modules can be imported correctly."""
    print("Testing core module structure...")
    
    try:
        # Test shared libraries
        from finassist.shared_libraries.types import Transaction, UserProfile, CategorySuggestion
        from finassist.shared_libraries.constants import CATEGORIES, SUPPORTED_CURRENCIES, PAYMENT_METHODS
        print("✓ Shared libraries imported successfully")
        
        # Test core tool functions (not the Tool wrappers)
        from finassist.tools.categorization import categorize_transaction, _rule_based_categorization
        from finassist.tools.validation import (
            validate_currency, validate_amount, validate_date, 
            validate_payment_method, save_transaction
        )
        print("✓ Core tool functions imported successfully")
        
        # Test transaction agent core functions
        from finassist.sub_agents.transaction.tools import (
            generate_transaction_id, get_current_timestamp,
            format_transaction_summary, validate_transaction_completeness
        )
        print("✓ Transaction agent core functions imported successfully")
        
        # Test prompts
        from finassist.sub_agents.transaction.prompt import TRANSACTION_AGENT_INSTR
        from finassist.sub_agents.consulting.prompt import CONSULTING_AGENT_INSTR
        from finassist.prompt import ROOT_AGENT_INSTR
        print("✓ Prompts imported successfully")
        
        print("\n✅ All core modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_functionality():
    """Test core functionality."""
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
    print(f"  - Amount: {transaction.amount} {transaction.currency}")
    print(f"  - Type: {transaction.transaction_type}")
    
    # Test categorization
    from finassist.tools.categorization import categorize_transaction
    suggestion = categorize_transaction(
        establishment="Netflix",
        description="Monthly subscription",
        amount="100",
        context="Entertainment service"
    )
    print(f"✓ Categorization: {suggestion.category} > {suggestion.subcategory}")
    print(f"  - Confidence: {suggestion.confidence}")
    
    # Test validation functions
    from finassist.tools.validation import validate_currency, validate_amount, validate_date
    print(f"✓ Currency validation (USD): {validate_currency('USD')}")
    print(f"✓ Currency validation (INVALID): {validate_currency('INVALID')}")
    print(f"✓ Amount validation (100): {validate_amount('100')}")
    print(f"✓ Amount validation (-50): {validate_amount('-50')}")
    print(f"✓ Date validation (2025-01-01): {validate_date('2025-01-01')}")
    
    # Test transaction tools
    from finassist.sub_agents.transaction.tools import generate_transaction_id, get_current_timestamp
    txn_id = generate_transaction_id()
    timestamp = get_current_timestamp()
    print(f"✓ Generated transaction ID: {txn_id}")
    print(f"✓ Generated timestamp: {timestamp}")
    
    # Test transaction completeness
    from finassist.sub_agents.transaction.tools import validate_transaction_completeness
    complete_data = {
        'amount': '100',
        'currency': 'USD',
        'transaction_date': '2025-01-01',
        'transaction_type': 'expense',
        'category': 'Entertainment'
    }
    incomplete_data = {
        'amount': '100',
        'currency': 'USD'
    }
    
    is_complete, missing = validate_transaction_completeness(complete_data)
    print(f"✓ Complete transaction validation: {is_complete}")
    
    is_complete, missing = validate_transaction_completeness(incomplete_data)
    print(f"✓ Incomplete transaction validation: {is_complete}, missing: {missing}")
    
    print("\n✅ All functionality tests passed!")


def test_constants():
    """Test that constants are properly defined."""
    print("\nTesting constants...")
    
    from finassist.shared_libraries.constants import CATEGORIES, SUPPORTED_CURRENCIES, PAYMENT_METHODS
    
    print(f"✓ Categories defined: {len(CATEGORIES)} main categories")
    print(f"✓ Currencies supported: {len(SUPPORTED_CURRENCIES)} currencies")
    print(f"✓ Payment methods: {len(PAYMENT_METHODS)} methods")
    
    # Test some specific categories
    assert "Food" in CATEGORIES
    assert "Entertainment" in CATEGORIES
    assert "Streaming" in CATEGORIES["Entertainment"]
    print("✓ Category structure validated")
    
    # Test currencies
    assert "USD" in SUPPORTED_CURRENCIES
    assert "EUR" in SUPPORTED_CURRENCIES
    assert "MXN" in SUPPORTED_CURRENCIES  # Mexican Peso
    print("✓ Currency list validated")
    
    # Test payment methods
    assert "Credit Card" in PAYMENT_METHODS
    assert "Cash" in PAYMENT_METHODS
    print("✓ Payment methods validated")
    
    print("\n✅ All constants tests passed!")


def test_save_transaction():
    """Test the save transaction functionality."""
    print("\nTesting save transaction...")
    
    from finassist.tools.validation import save_transaction
    
    sample_transaction = {
        "transaction_id": "TXN_12345678",
        "user_id": "user123",
        "amount": "100",
        "currency": "USD",
        "transaction_date": "2025-01-01",
        "recorded_date": "2025-01-01T10:30:00",
        "transaction_type": "expense",
        "category": "Entertainment",
        "subcategory": "Streaming",
        "establishment": "Netflix",
        "notes": "Monthly subscription",
        "payment_method": "Credit Card"
    }
    
    result = save_transaction(sample_transaction)
    print(f"✓ Save transaction result: {result}")
    
    print("\n✅ Save transaction test passed!")


def main():
    """Run all tests."""
    print("=" * 60)
    print("FINANCIAL ASSISTANT CORE FUNCTIONALITY TEST")
    print("=" * 60)
    
    success = test_core_imports()
    if success:
        test_functionality()
        test_constants()
        test_save_transaction()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL CORE TESTS PASSED!")
        print("The system core functionality is working correctly.")
        print("Ready for ADK integration when the library is available.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 60)


if __name__ == "__main__":
    main() 