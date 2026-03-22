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

from moneypoly.player import Player

def test_give_loan_deducts_funds():
    """Test that issuing a loan deducts the amount from the bank's reserves."""
    bank = Bank()
    player = Player("Alice", balance=0)
    initial_funds = bank.get_balance()
    
    bank.give_loan(player, 500)
    
    assert player.balance == 500
    assert bank.get_balance() == initial_funds - 500
