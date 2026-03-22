"""
Race Management Module (M_Race)
Sets up races (type, entry fee, prize pool, difficulty). Registers racers for a race.
Receives valid racers from the Registration and Crew modules. Checks requirements using the Inventory module.
"""

class Race:
    def __init__(self, name, race_type, entry_fee, prize_pool, min_speed):
        self.name = name
        self.race_type = race_type
        self.entry_fee = entry_fee
        self.prize_pool = prize_pool
        self.min_speed = min_speed
        self.participants = []

class RaceManagementModule:
    def __init__(self, registration_module, inventory_module):
        self.races = {}
        self.reg_module = registration_module
        self.inv_module = inventory_module

    def create_race(self, name, race_type, entry_fee, prize_pool, min_speed):
        """Creates a new race event."""
        if name in self.races:
            raise ValueError(f"Race {name} already exists.")
        race = Race(name, race_type, entry_fee, prize_pool, min_speed)
        self.races[name] = race
        return race

    def register_for_race(self, race_name, racer_id):
        """Registers a racer for a race after checking requirements and balances."""
        race = self.races.get(race_name)
        racer = self.reg_module.get_racer(racer_id)
        
        if not race or not racer:
            return False

        # Check balance for entry fee
        if racer.balance < race.entry_fee:
            return False

        # Check inventory requirements
        if not self.inv_module.validate_car_requirements(racer_id, race.min_speed):
            return False

        # Deduct entry fee and add to participants
        racer.balance -= race.entry_fee
        race.participants.append(racer)
        return True

    def get_participants(self, race_name):
        """Returns the list of participants for a given race."""
        race = self.races.get(race_name)
        return race.participants if race else []
