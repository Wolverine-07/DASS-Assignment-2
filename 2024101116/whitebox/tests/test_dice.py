import pytest
from unittest.mock import patch
from moneypoly.dice import Dice

def test_dice_range_includes_six():
    """Test that dice can roll a 6 (range 1 to 6)."""
    dice = Dice()
    with patch('random.randint', return_value=6) as mock_randint:
        dice.roll()
        # Dice should request a random integer between 1 and 6
        mock_randint.assert_called_with(1, 6)
