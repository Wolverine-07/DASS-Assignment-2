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

def test_pay_rent_transfers_money():
    """Test that paying rent deducts from tenant and adds to owner."""
    game = Game(["Alice", "Bob"])
    tenant = game.players[0]
    owner = game.players[1]
    
    tenant.balance = 1000
    owner.balance = 1000
    
    prop = Property("Boardwalk", position=39, price=400, base_rent=50)
    prop.owner = owner
    owner.add_property(prop)
    
    game.pay_rent(tenant, prop)
    
    assert tenant.balance == 950
    assert owner.balance == 1050
