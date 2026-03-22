"""
Crew Management Module (M_Crew)
Handles forming and managing racing crews (groups of racers).
"""

class Crew:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, racer):
        """Adds a racer to the crew."""
        if racer not in self.members:
            self.members.append(racer)
            racer.crew = self.name

    def remove_member(self, racer):
        """Removes a racer from the crew."""
        if racer in self.members:
            self.members.remove(racer)
            racer.crew = None

class CrewManagementModule:
    def __init__(self):
        self.crews = {}

    def create_crew(self, name):
        """Creates a new crew."""
        if name in self.crews:
            raise ValueError(f"Crew {name} already exists.")
        crew = Crew(name)
        self.crews[name] = crew
        return crew

    def get_crew(self, name):
        """Retrieves a crew by name."""
        return self.crews.get(name)

    def add_racer_to_crew(self, racer, crew_name):
        """Adds a racer to a specific crew."""
        crew = self.get_crew(crew_name)
        if crew:
            crew.add_member(racer)
        else:
            raise ValueError(f"Crew {crew_name} not found.")
