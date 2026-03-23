"""
Betting Module (Custom 1)
Allows racers to place bets on other racers before a race starts.
Calculates payouts and distributes them after a race concludes.
"""

class Bet:
    def __init__(self, bettor_id, race_name, predicted_winner_id, amount):
        self.bettor_id = bettor_id
        self.race_name = race_name
        self.predicted_winner_id = predicted_winner_id
        self.amount = amount

class BettingModule:
    def __init__(self, registration_module):
        self.reg_module = registration_module
        self.active_bets = []
        self.completed_bets = []

    def place_bet(self, bettor_id, race_name, predicted_winner_id, amount):
        """Places a bet if the bettor has enough balance."""
        if amount <= 0:
            return False
            
        bettor = self.reg_module.get_racer(bettor_id)
        if not bettor or bettor.balance < amount:
            return False
            
        bettor.balance -= amount
        bet = Bet(bettor_id, race_name, predicted_winner_id, amount)
        self.active_bets.append(bet)
        return True

    def process_race_results(self, race_result):
        """
        Receives notification of a race result from the Results Module.
        Calculates and distributes payouts for winning bets.
        """
        # We process bets for this specific race
        bets_to_process = [b for b in self.active_bets if b.race_name == race_result.race_name]
        
        # Simple payout: 2x the bet amount for a correct prediction
        for bet in bets_to_process:
            if bet.predicted_winner_id == race_result.winner_id:
                bettor = self.reg_module.get_racer(bet.bettor_id)
                if bettor:
                    payout = bet.amount * 2
                    bettor.balance += payout
            
            self.active_bets.remove(bet)
            self.completed_bets.append(bet)
