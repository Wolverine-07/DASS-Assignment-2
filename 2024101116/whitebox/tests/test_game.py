import pytest
from moneypoly.game import Game
from moneypoly.player import Player
from moneypoly.property import Property

def test_buy_property_exact_balance():
    """Test that a player can buy a property if they have exactly enough money."""
    game = Game(["Alice", "Bob"])
    player = game.players[0]
    
    # Set player's balance to exactly 200
    player.balance = 200
    
    # Create a property that costs exactly 200
    prop = Property("Reading Railroad", position=5, price=200, base_rent=25)
    
    # The purchase should succeed
    success = game.buy_property(player, prop)
    
    assert success is True
    assert player.balance == 0
    assert prop.owner == player
    assert prop in player.properties
