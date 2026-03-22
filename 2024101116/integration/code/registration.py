"""
Racer Registration Module (M_Reg)
Registers new racers with basic details (e.g., Racer ID, Name, Starting Balance, Starter Car).
"""

class Racer:
    def __init__(self, racer_id, name, balance, starter_car):
        self.racer_id = racer_id
        self.name = name
        self.balance = balance
        self.car = starter_car
        self.crew = None

class RegistrationModule:
    def __init__(self):
        self.racers = {}

    def register_racer(self, racer_id, name, balance, starter_car):
        """Registers a new racer."""
        if racer_id in self.racers:
            raise ValueError(f"Racer {racer_id} already exists.")
        racer = Racer(racer_id, name, balance, starter_car)
        self.racers[racer_id] = racer
        return racer

    def get_racer(self, racer_id):
        """Retrieves racer details."""
        return self.racers.get(racer_id)
