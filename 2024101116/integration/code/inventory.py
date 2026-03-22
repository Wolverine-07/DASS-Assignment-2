"""
Inventory & Garage Module (M_Inv)
Manages cars, upgrades, and parts for each racer. Allows racers to buy/sell/equip parts.
Validates if a racer's car meets race requirements.
"""

class Car:
    def __init__(self, name, base_speed):
        self.name = name
        self.base_speed = base_speed
        self.parts = []

    def equip_part(self, part):
        self.parts.append(part)

    def get_speed(self):
        return self.base_speed + sum(p.speed_boost for p in self.parts)


class Part:
    def __init__(self, name, speed_boost, price):
        self.name = name
        self.speed_boost = speed_boost
        self.price = price


class InventoryModule:
    def __init__(self):
        # Maps racer_id to a list of cars and parts they own
        self.racer_inventories = {}
        # Maps racer_id to their currently active car
        self.active_cars = {}
        # Available parts in the shop
        self.shop_parts = {}

    def setup_inventory(self, racer_id, starter_car):
        """Initializes a racer's inventory with their starter car."""
        self.racer_inventories[racer_id] = {'cars': [starter_car], 'parts': []}
        self.active_cars[racer_id] = starter_car

    def add_part_to_shop(self, part):
        """Adds a part to the available shop inventory."""
        self.shop_parts[part.name] = part

    def buy_part(self, racer, part_name):
        """Allows a racer to buy a part if they have enough balance."""
        if part_name not in self.shop_parts:
            raise ValueError(f"Part {part_name} not available in shop.")
            
        part = self.shop_parts[part_name]
        if racer.balance >= part.price:
            racer.balance -= part.price
            self.racer_inventories[racer.racer_id]['parts'].append(part)
            return True
        return False

    def equip_part(self, racer_id, part_name):
        """Equips a part to the racer's currently active car."""
        inventory = self.racer_inventories.get(racer_id)
        if not inventory:
            return False
            
        # Find the part in their inventory
        part_to_equip = next((p for p in inventory['parts'] if p.name == part_name), None)
        if part_to_equip:
            active_car = self.active_cars.get(racer_id)
            if active_car:
                active_car.equip_part(part_to_equip)
                inventory['parts'].remove(part_to_equip)
                return True
        return False

    def validate_car_requirements(self, racer_id, min_speed):
        """
        Validates if a racer's active car meets the required minimum speed for a race.
        Used by the Race Management Module.
        """
        active_car = self.active_cars.get(racer_id)
        if active_car and active_car.get_speed() >= min_speed:
            return True
        return False
