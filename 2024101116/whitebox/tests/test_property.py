import pytest
from moneypoly.property import Property
from moneypoly.player import Player
from moneypoly.board import Board

def test_all_owned_by_requires_all_properties():
    """Test that all_owned_by returns False if the player only owns some properties in the group."""
    board = Board()
    player = Player("Alice")
    
    # Get properties from the 'brown' group (Mediterranean and Baltic)
    mediterranean = board.get_property_at(1)
    baltic = board.get_property_at(3)
    
    # Give Alice Mediterranean but not Baltic
    mediterranean.owner = player
    player.add_property(mediterranean)
    
    # all_owned_by should be False because she doesn't own all 'brown' properties
    assert not mediterranean.group.all_owned_by(player)
    
    # Give Alice Baltic
    baltic.owner = player
    player.add_property(baltic)
    
    # Now it should be True
    assert mediterranean.group.all_owned_by(player)
