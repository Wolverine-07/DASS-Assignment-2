"""
Reputation Module (Custom 2)
Tracks a racer's reputation in the underground scene based on race outcomes.
High reputation is generally required for exclusive races or crews.
"""

class ReputationModule:
    def __init__(self, registration_module):
        self.reg_module = registration_module
        # Initialize default reputation (50) for racers
        self.reputations = {}

    def get_reputation(self, racer_id):
        """Returns the reputation score for a racer, defaulting to 50 if new."""
        # Auto-initialize if they exist in registration but not here yet
        if racer_id not in self.reputations and self.reg_module.get_racer(racer_id):
            self.reputations[racer_id] = 50
        return self.reputations.get(racer_id, 0)

    def process_race_results(self, race_result):
        """
        Receives notification of a race result from the Results Module.
        Increases the winner's reputation and slightly decreases losers' reputations.
        """
        winner_id = race_result.winner_id
        
        for participant_id in race_result.participants:
            current_rep = self.get_reputation(participant_id)
            if participant_id == winner_id:
                # Winner gains 10 rep
                self.reputations[participant_id] = current_rep + 10
            else:
                # Losers lose 2 rep
                self.reputations[participant_id] = max(0, current_rep - 2)

    def is_eligible_for_exclusive(self, racer_id, min_reputation):
        """Checks if a racer meets the minimum reputation for an exclusive event."""
        return self.get_reputation(racer_id) >= min_reputation
