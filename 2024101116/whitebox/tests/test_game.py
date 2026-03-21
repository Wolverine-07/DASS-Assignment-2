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

def test_find_winner_returns_richest():
    """Test that find_winner returns the player with the highest net worth, not the lowest."""
    game = Game(["Alice", "Bob", "Charlie"])
    
    game.players[0].balance = 500
    game.players[1].balance = 2000
    game.players[2].balance = 1500
    
    winner = game.find_winner()
    assert winner.name == "Bob"

def test_trade_credits_seller_cash():
    """Test that a trade correctly deductions from buyer and adds to seller."""
    game = Game(["Seller", "Buyer"])
    seller = game.players[0]
    buyer = game.players[1]
    
    seller.balance = 500
    buyer.balance = 1000
    
    prop = Property("Park Place", position=37, price=350, base_rent=35)
    prop.owner = seller
    seller.add_property(prop)
    
    success = game.trade(seller, buyer, prop, 300)
    
    assert success is True
    assert buyer.balance == 700
    assert seller.balance == 800
    assert prop.owner == buyer
