"""
Mission & Event Planning Module (M_Plan)
Manages special events or long-term missions. Awards bonuses for completion.
Receives race results from the Results Module to track mission progress.
"""

class Mission:
    def __init__(self, name, required_wins, bonus_reward):
        self.name = name
        self.required_wins = required_wins
        self.bonus_reward = bonus_reward
        self.completed_by = set()

class MissionPlanningModule:
    def __init__(self, registration_module):
        self.missions = {}
        # Maps racer_id to a dict of mission_name -> wins
        self.racer_progress = {} 
        self.reg_module = registration_module

    def create_mission(self, name, required_wins, bonus_reward):
        """Creates a new long-term mission."""
        if name in self.missions:
            raise ValueError(f"Mission {name} already exists.")
        mission = Mission(name, required_wins, bonus_reward)
        self.missions[name] = mission
        return mission

    def enroll_racer(self, racer_id, mission_name):
        """Enrolls a racer in a specific mission."""
        if mission_name not in self.missions:
            raise ValueError(f"Mission {mission_name} not found.")
        
        if racer_id not in self.racer_progress:
            self.racer_progress[racer_id] = {}
            
        if mission_name not in self.racer_progress[racer_id]:
            self.racer_progress[racer_id][mission_name] = 0
            return True
        return False

    def record_race_result(self, race_result):
        """
        Receives notification of a race result.
        Updates mission progress for the winner and awards bonuses if completed.
        """
        winner_id = race_result.winner_id
        if winner_id in self.racer_progress:
            for mission_name, current_wins in self.racer_progress[winner_id].items():
                mission = self.missions.get(mission_name)
                
                # If they haven't completed it yet
                if mission and winner_id not in mission.completed_by:
                    self.racer_progress[winner_id][mission_name] += 1
                    
                    # Check if they just completed it
                    if self.racer_progress[winner_id][mission_name] >= mission.required_wins:
                        mission.completed_by.add(winner_id)
                        # Award the bonus using the registration module reference
                        racer = self.reg_module.get_racer(winner_id)
                        if racer:
                            racer.balance += mission.bonus_reward
