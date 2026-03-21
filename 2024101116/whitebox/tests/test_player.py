import pytest
from moneypoly.player import Player
from moneypoly.property import Property

def test_net_worth_includes_properties():
    """Test that a player's net worth includes both cash balance and property values."""
    player = Player("Alice", balance=1500)
    
    # Create a dummy property worth $400
    prop = Property("Boardwalk", position=39, price=400, base_rent=50)
    player.add_property(prop)
    
    # Net worth should be 1500 (balance) + 400 (property) = 1900
    assert player.net_worth() == 1900

def test_passing_go_awards_salary():
    """Test that a player receives GO salary when passing OR landing on GO."""
    player = Player("Bob", balance=1500)
    
    # Put Bob near GO
    player.position = 38
    
    # Move him 5 spaces. 38 + 5 = 43 % 40 = 3
    # He should collect GO salary (200)
    player.move(5)
    
    assert player.position == 3
    assert player.balance == 1700
