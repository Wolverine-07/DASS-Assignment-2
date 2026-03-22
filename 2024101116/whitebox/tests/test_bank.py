import pytest
from moneypoly.bank import Bank

def test_bank_collect_ignores_negatives():
    """Test that Bank.collect() silently ignores negative amounts."""
    bank = Bank()
    initial_funds = bank.get_balance()
    
    # Attempt to collect a negative amount
    bank.collect(-100)
    
    # Funds should not decrease
    assert bank.get_balance() == initial_funds
