"""
Race Results Module (M_Results)
Calculates the outcome of a race.
Receives race data from the Race Module. Sends results to the Mission Planning Module.
"""

class RaceResult:
    def __init__(self, race_name, winner_id, participants):
        self.race_name = race_name
        self.winner_id = winner_id
        self.participants = participants

class ResultsModule:
    def __init__(self, race_module, mission_planning_module=None):
        self.race_module = race_module
        self.mission_module = mission_planning_module
        self.past_results = []

    def set_mission_module(self, mission_planning_module):
        """Sets the mission module (useful for resolving circular dependencies)."""
        self.mission_module = mission_planning_module

    def calculate_race_outcome(self, race_name, winner_id=None):
        """
        Calculates the outcome of a race and awards the prize pool.
        For predictability in tests, the winner_id can be specified, 
        otherwise the first participant defaults to winning.
        """
        race = self.race_module.races.get(race_name)
        if not race:
            raise ValueError(f"Race {race_name} not found.")

        if not race.participants:
            raise ValueError(f"No participants in race {race_name}.")

        if winner_id:
            winner = next((p for p in race.participants if p.racer_id == winner_id), None)
            if not winner:
                raise ValueError(f"Racer {winner_id} is not in the race.")
        else:
            winner = race.participants[0]
        
        # Award prize
        winner.balance += race.prize_pool
        
        result = RaceResult(race_name, winner.racer_id, [p.racer_id for p in race.participants])
        self.past_results.append(result)

        # Notify mission planning
        if self.mission_module:
            self.mission_module.record_race_result(result)
            
        return result
