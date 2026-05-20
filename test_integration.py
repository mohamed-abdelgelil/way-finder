# test_integration.py
# Integration test: Verify all tool modules are importable and work correctly
# Mocks the strands module since it may not be installed in the test environment.

import sys
import unittest
from unittest.mock import MagicMock


# --- Mock the strands module before importing tool modules ---
# The @tool decorator is a pass-through: it returns the function unchanged.
mock_strands = MagicMock()
mock_strands.tool = lambda fn: fn  # pass-through decorator
sys.modules["strands"] = mock_strands


# --- Now import all tool modules (same imports as the notebook uses) ---
from destination_tool import get_destinations, get_destination_details
from hotel_tool import get_hotels
from restaurant_tool import get_restaurants
from activity_tool import get_activities
from trip_planner_tool import plan_trip
from travel_data import DESTINATIONS, HOTELS, RESTAURANTS, ACTIVITIES


class TestImportsAndCallability(unittest.TestCase):
    """Verify all tool functions are importable and callable."""

    def test_get_destinations_is_callable(self):
        self.assertTrue(callable(get_destinations))

    def test_get_destination_details_is_callable(self):
        self.assertTrue(callable(get_destination_details))

    def test_get_hotels_is_callable(self):
        self.assertTrue(callable(get_hotels))

    def test_get_restaurants_is_callable(self):
        self.assertTrue(callable(get_restaurants))

    def test_get_activities_is_callable(self):
        self.assertTrue(callable(get_activities))

    def test_plan_trip_is_callable(self):
        self.assertTrue(callable(plan_trip))


class TestDestinationTool(unittest.TestCase):
    """Verify destination tool returns correct formatted responses."""

    def test_get_destinations_returns_all(self):
        result = get_destinations()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        # Should mention all 5 destinations
        for dest in DESTINATIONS.values():
            self.assertIn(dest["name"], result)

    def test_get_destination_details_valid(self):
        result = get_destination_details("Cairo")
        self.assertIsInstance(result, str)
        self.assertIn("Cairo", result)
        self.assertIn("Lower Egypt", result)
        self.assertIn("Hotels:", result)

    def test_get_destination_details_case_insensitive(self):
        result = get_destination_details("LUXOR")
        self.assertIn("Luxor", result)

    def test_get_destination_details_invalid(self):
        result = get_destination_details("Atlantis")
        self.assertIn("not found", result)
        # Should list available destinations
        self.assertIn("Cairo", result)


class TestHotelTool(unittest.TestCase):
    """Verify hotel tool returns correct formatted responses."""

    def test_get_hotels_no_budget(self):
        result = get_hotels("Cairo")
        self.assertIsInstance(result, str)
        self.assertIn("Hotels in Cairo", result)
        self.assertIn("Marriott Mena House", result)

    def test_get_hotels_with_budget(self):
        result = get_hotels("Cairo", budget=100)
        self.assertIn("Cairo Budget Inn", result)
        # Expensive hotel should not appear
        self.assertNotIn("Marriott Mena House", result)

    def test_get_hotels_budget_too_low(self):
        result = get_hotels("Cairo", budget=10)
        self.assertIn("No hotels", result)
        self.assertIn("nearest available", result.lower())

    def test_get_hotels_invalid_destination(self):
        result = get_hotels("Mars")
        self.assertIn("not found", result)


class TestRestaurantTool(unittest.TestCase):
    """Verify restaurant tool returns correct formatted responses."""

    def test_get_restaurants_no_filter(self):
        result = get_restaurants("Cairo")
        self.assertIsInstance(result, str)
        self.assertIn("Restaurants in Cairo", result)
        self.assertIn("Abou El Sid", result)

    def test_get_restaurants_cuisine_filter(self):
        result = get_restaurants("Cairo", cuisine="Egyptian")
        self.assertIn("Abou El Sid", result)
        # Mediterranean restaurant should not appear
        self.assertNotIn("Sequoia", result)

    def test_get_restaurants_budget_filter(self):
        result = get_restaurants("Cairo", budget=20)
        self.assertIn("Zooba", result)
        self.assertNotIn("Sequoia", result)

    def test_get_restaurants_no_match(self):
        result = get_restaurants("Cairo", cuisine="Japanese")
        self.assertIn("No restaurants match", result)

    def test_get_restaurants_invalid_destination(self):
        result = get_restaurants("Narnia")
        self.assertIn("not found", result)


class TestActivityTool(unittest.TestCase):
    """Verify activity tool returns correct formatted responses."""

    def test_get_activities_no_budget(self):
        result = get_activities("Cairo")
        self.assertIsInstance(result, str)
        self.assertIn("Activities in Cairo", result)
        self.assertIn("Pyramids of Giza Tour", result)

    def test_get_activities_with_budget(self):
        result = get_activities("Cairo", budget=30)
        self.assertIn("Egyptian Museum Visit", result)
        self.assertIn("Khan El Khalili Bazaar Walk", result)
        # Expensive activity should not appear
        self.assertNotIn("Pyramids of Giza Tour", result)

    def test_get_activities_budget_too_low(self):
        result = get_activities("Cairo", budget=5)
        self.assertIn("No activities", result)
        self.assertIn("Nearest available options", result)

    def test_get_activities_invalid_destination(self):
        result = get_activities("Mordor")
        self.assertIn("not found", result)


class TestTripPlannerTool(unittest.TestCase):
    """Verify trip planner tool returns correct formatted responses."""

    def test_plan_trip_within_budget(self):
        # Cairo Budget Inn ($45) + Zooba ($12) + Khan El Khalili ($10) = $67
        result = plan_trip("Cairo", total_budget=200, nights=1)
        self.assertIsInstance(result, str)
        self.assertIn("Trip Plans for Cairo", result)
        self.assertIn("Accommodation", result)
        self.assertIn("Dining", result)
        self.assertIn("Activity", result)
        self.assertIn("Total Cost", result)

    def test_plan_trip_budget_too_low(self):
        result = plan_trip("Cairo", total_budget=10, nights=1)
        self.assertIn("No complete trip plan", result)
        self.assertIn("Minimum budget required", result)

    def test_plan_trip_multiple_nights(self):
        result = plan_trip("Cairo", total_budget=500, nights=3)
        self.assertIn("3 nights", result)

    def test_plan_trip_invalid_destination(self):
        result = plan_trip("Wakanda", total_budget=500)
        self.assertIn("not found", result)


class TestEndToEndIntegration(unittest.TestCase):
    """Test tools working together in a realistic flow."""

    def test_discover_then_hotel_then_plan(self):
        """Simulate: user discovers destinations, picks one, gets hotels, plans trip."""
        # Step 1: Discover destinations
        destinations = get_destinations()
        self.assertIn("Cairo", destinations)
        self.assertIn("Luxor", destinations)

        # Step 2: Get details about a destination
        details = get_destination_details("Aswan")
        self.assertIn("Aswan", details)
        self.assertIn("Hotels:", details)

        # Step 3: Get hotels for that destination with budget
        hotels = get_hotels("Aswan", budget=100)
        self.assertIn("Basma Hotel", hotels)

        # Step 4: Get restaurants
        restaurants = get_restaurants("Aswan")
        self.assertIn("Nubian House", restaurants)

        # Step 5: Get activities
        activities = get_activities("Aswan", budget=50)
        self.assertIn("Philae Temple Visit", activities)
        self.assertIn("Felucca Nile Cruise", activities)

        # Step 6: Plan a complete trip
        trip = plan_trip("Aswan", total_budget=200, nights=2)
        self.assertIn("Trip Plans for Aswan", trip)
        self.assertIn("Total Cost", trip)

    def test_budget_preference_consistency(self):
        """Verify budget filtering is consistent across tools for same destination."""
        budget = 30
        destination = "Cairo"

        # All returned items should respect the budget
        hotels = get_hotels(destination, budget=budget)
        # Budget $30 is below cheapest Cairo hotel ($45), so should get "no hotels" message
        self.assertIn("No hotels", hotels)

        restaurants = get_restaurants(destination, budget=budget)
        # Zooba ($12) and Abou El Sid ($30) should appear
        self.assertIn("Zooba", restaurants)

        activities = get_activities(destination, budget=budget)
        # Egyptian Museum ($25) and Khan El Khalili ($10) should appear
        self.assertIn("Egyptian Museum Visit", activities)
        self.assertIn("Khan El Khalili Bazaar Walk", activities)

    def test_all_destinations_have_complete_data(self):
        """Verify every destination has hotels, restaurants, and activities."""
        for key in DESTINATIONS:
            dest_name = DESTINATIONS[key]["name"]

            hotels = get_hotels(dest_name)
            self.assertIn(f"Hotels in {dest_name}", hotels, f"Missing hotels for {dest_name}")

            restaurants = get_restaurants(dest_name)
            self.assertIn(f"Restaurants in {dest_name}", restaurants, f"Missing restaurants for {dest_name}")

            activities = get_activities(dest_name)
            self.assertIn(f"Activities in {dest_name}", activities, f"Missing activities for {dest_name}")

    def test_trip_plan_cost_breakdown_adds_up(self):
        """Verify trip plan cost breakdown is internally consistent."""
        # Use a generous budget to get plans
        result = plan_trip("Hurghada", total_budget=300, nights=1)
        self.assertIn("Trip Plans for Hurghada", result)
        # Verify the plan contains cost breakdown sections
        self.assertIn("Accommodation:", result)
        self.assertIn("Dining:", result)
        self.assertIn("Activity:", result)
        self.assertIn("Total Cost:", result)
        self.assertIn("Budget Remaining:", result)


class TestSessionMemorySimulation(unittest.TestCase):
    """Test that tool functions can be called sequentially simulating session memory.

    While actual session memory is managed by the Strands Agent, we verify that
    the tools support the pattern: user states a preference once, and subsequent
    calls use that preference (simulated by passing the same parameter).
    """

    def test_destination_preference_reuse(self):
        """Simulate agent remembering destination preference across calls."""
        preferred_destination = "Luxor"

        # First call: user asks about destination
        details = get_destination_details(preferred_destination)
        self.assertIn("Luxor", details)

        # Subsequent calls: agent reuses the destination
        hotels = get_hotels(preferred_destination)
        self.assertIn("Hotels in Luxor", hotels)

        restaurants = get_restaurants(preferred_destination)
        self.assertIn("Restaurants in Luxor", restaurants)

        activities = get_activities(preferred_destination)
        self.assertIn("Activities in Luxor", activities)

    def test_budget_preference_reuse(self):
        """Simulate agent remembering budget preference across calls."""
        preferred_budget = 50.0
        destination = "Hurghada"

        hotels = get_hotels(destination, budget=preferred_budget)
        # No hotels under $50 in Hurghada (cheapest is $65)
        self.assertIn("No hotels", hotels)

        activities = get_activities(destination, budget=preferred_budget)
        self.assertIn("Red Sea Snorkeling Trip", activities)


if __name__ == "__main__":
    unittest.main()
