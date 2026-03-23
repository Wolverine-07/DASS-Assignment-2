import pytest
from integration.code.registration import RegistrationModule, Racer
from integration.code.crew_management import CrewManagementModule
from integration.code.inventory import InventoryModule, Car, Part
from integration.code.race_management import RaceManagementModule
from integration.code.results import ResultsModule
from integration.code.mission_planning import MissionPlanningModule
from integration.code.betting import BettingModule
from integration.code.reputation import ReputationModule

class TestStreetRaceIntegration:
    @pytest.fixture
    def system(self):
        """Sets up the entire integrated system."""
        reg = RegistrationModule()
        crew = CrewManagementModule()
        inv = InventoryModule()
        race_mgr = RaceManagementModule(reg, inv)
        mission = MissionPlanningModule(reg)
        results = ResultsModule(race_mgr, mission)
        betting = BettingModule(reg)
        rep = ReputationModule(reg)
        
        return {
            'reg': reg,
            'crew': crew,
            'inv': inv,
            'race_mgr': race_mgr,
            'results': results,
            'mission': mission,
            'betting': betting,
            'rep': rep
        }

    def test_registration_to_crew(self, system):
        """Test racers registering and joining a crew."""
        racer1 = system['reg'].register_racer("r1", "Dom", 1000, Car("Charger", 150))
        racer2 = system['reg'].register_racer("r2", "Brian", 1000, Car("Eclipse", 140))
        
        system['crew'].create_crew("Family")
        system['crew'].add_racer_to_crew(racer1, "Family")
        system['crew'].add_racer_to_crew(racer2, "Family")
        
        crew = system['crew'].get_crew("Family")
        assert len(crew.members) == 2
        assert racer1.crew == "Family"

    def test_inventory_parts_management(self, system):
        """Test buying and equipping parts to meet race requirements."""
        car = Car("Civic", 100)
        racer = system['reg'].register_racer("r1", "Letty", 500, car)
        system['inv'].setup_inventory("r1", car)
        
        turbo = Part("Turbo", speed_boost=50, price=300)
        system['inv'].add_part_to_shop(turbo)
        
        # Racer buys and equips part
        # Initial speed 100, requirement 140 -> False
        assert not system['inv'].validate_car_requirements("r1", 140)
        
        assert system['inv'].buy_part(racer, "Turbo")
        assert racer.balance == 200
        assert system['inv'].equip_part("r1", "Turbo")
        
        # New speed 150 -> True
        assert system['inv'].validate_car_requirements("r1", 140)

    def test_race_registration_and_fees(self, system):
        """Test race creation and validating entry fees/requirements."""
        car = Car("RX-7", 130)
        racer = system['reg'].register_racer("r1", "Han", 1000, car)
        system['inv'].setup_inventory("r1", car)
        
        system['race_mgr'].create_race("Drift King", "Drift", entry_fee=200, prize_pool=1000, min_speed=120)
        
        # Valid registration
        assert system['race_mgr'].register_for_race("Drift King", "r1")
        assert racer.balance == 800
        
        # Invalid registration (too slow)
        car2 = Car("Beetle", 90)
        racer_slow = system['reg'].register_racer("r2", "Sean", 1000, car2)
        system['inv'].setup_inventory("r2", car2)
        assert not system['race_mgr'].register_for_race("Drift King", "r2")

    def test_mission_completion_via_results(self, system):
        """Test that winning a race records progress and awards mission bonuses."""
        racer = system['reg'].register_racer("r1", "Dom", 1000, Car("Charger", 150))
        system['race_mgr'].create_race("Race 1", "Sprint", 100, 500, 100)
        system['race_mgr'].register_for_race("Race 1", "r1")
        
        system['mission'].create_mission("Rookie", required_wins=1, bonus_reward=1000)
        system['mission'].enroll_racer("r1", "Rookie")
        
        system['results'].calculate_race_outcome("Race 1", winner_id="r1")
        
        # Initial 1000 - 100 entry + 500 prize + 1000 bonus = 2400
        assert racer.balance == 2400

    def test_custom_betting_module(self, system):
        """Test the custom betting module processes wagers correctly on race outcomes."""
        racer1 = system['reg'].register_racer("r1", "Racer1", 1000, Car("Car1", 100))
        racer2 = system['reg'].register_racer("r2", "Racer2", 1000, Car("Car2", 100))
        bettor = system['reg'].register_racer("b1", "Bettor", 1000, Car("Car3", 100))
        
        system['race_mgr'].create_race("Big Race", "Sprint", 100, 500, 50)
        system['race_mgr'].register_for_race("Big Race", "r1")
        system['race_mgr'].register_for_race("Big Race", "r2")
        
        # Bettor wagers $200 on r2
        assert system['betting'].place_bet("b1", "Big Race", predicted_winner_id="r2", amount=200)
        assert bettor.balance == 800
        
        # Race resolves, r2 wins
        result = system['results'].calculate_race_outcome("Big Race", winner_id="r2")
        system['betting'].process_race_results(result)
        
        # Bettor wins 2x their bet -> 800 + 400 = 1200
        assert bettor.balance == 1200

    def test_custom_reputation_module(self, system):
        """Test the custom reputation module adjustments based on race results."""
        racer1 = system['reg'].register_racer("r1", "Winner", 1000, Car("Car1", 100))
        racer2 = system['reg'].register_racer("r2", "Loser", 1000, Car("Car2", 100))
        
        system['race_mgr'].create_race("Street Cup", "Circuit", 100, 500, 50)
        system['race_mgr'].register_for_race("Street Cup", "r1")
        system['race_mgr'].register_for_race("Street Cup", "r2")
        
        result = system['results'].calculate_race_outcome("Street Cup", winner_id="r1")
        system['rep'].process_race_results(result)
        
        # Winner gains 10 rep, Loser loses 2 rep (base 50)
        assert system['rep'].get_reputation("r1") == 60
        assert system['rep'].get_reputation("r2") == 48

    def test_full_system_integration(self, system):
        """Comprehensive E2E test crossing all 8 modules."""
        # 1. Registration
        dom = system['reg'].register_racer("r1", "Dom", 1000, Car("Charger", 150))
        brian = system['reg'].register_racer("r2", "Brian", 1000, Car("Supra", 160))
        roman = system['reg'].register_racer("r3", "Roman", 1000, Car("Eclipse", 100))
        
        # 2. Crew
        system['crew'].create_crew("Family")
        system['crew'].add_racer_to_crew(dom, "Family")
        system['crew'].add_racer_to_crew(brian, "Family")
        
        # 3. Inventory upgrades
        system['inv'].setup_inventory("r1", dom.car)
        system['inv'].setup_inventory("r2", brian.car)
        system['inv'].setup_inventory("r3", roman.car)
        
        nos = Part("NOS", speed_boost=50, price=300)
        system['inv'].add_part_to_shop(nos)
        system['inv'].buy_part(roman, "NOS")
        system['inv'].equip_part("r3", "NOS")  # Speed is now 150
        
        # 4. Missions
        system['mission'].create_mission("First Win", required_wins=1, bonus_reward=1000)
        system['mission'].enroll_racer("r3", "First Win")
        
        # 5. Race Management
        system['race_mgr'].create_race("Final Boss", "Sprint", entry_fee=200, prize_pool=5000, min_speed=140)
        system['race_mgr'].register_for_race("Final Boss", "r1")
        system['race_mgr'].register_for_race("Final Boss", "r2")
        system['race_mgr'].register_for_race("Final Boss", "r3")
        
        # 6. Betting (Dom bets on Brian)
        system['betting'].place_bet("r1", "Final Boss", predicted_winner_id="r2", amount=100)
        
        # 7. Results (Brian wins)
        result = system['results'].calculate_race_outcome("Final Boss", winner_id="r2")
        
        # Process post-race hooks
        system['betting'].process_race_results(result)
        system['rep'].process_race_results(result)
        # (Mission processing is handled automatically by ResultsModule -> Mission module)
        
        # Assertions
        assert result.winner_id == "r2"
        # Brian: 1000 - 200 entry + 5000 prize = 5800
        assert brian.balance == 5800
        # Dom: 1000 - 200 entry - 100 bet + 200 payout = 900
        assert dom.balance == 900
        
        # Mission progress for Roman -> no progress because he didn't win
        # 1000 - 300 (NOS) - 200 (entry) = 500
        assert roman.balance == 500
        
        # Reputation
        assert system['rep'].get_reputation("r2") == 60
        assert system['rep'].get_reputation("r1") == 48
        assert system['rep'].get_reputation("r3") == 48
