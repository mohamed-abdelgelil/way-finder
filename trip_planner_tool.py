# trip_planner_tool.py
# Trip planning tool for the Egypt Travel Agent

from strands import tool
from travel_data import HOTELS, RESTAURANTS, ACTIVITIES, DESTINATIONS


def _normalize_destination(destination: str) -> str:
    """Normalize destination name for case-insensitive dictionary lookup."""
    return destination.strip().lower()


@tool
def plan_trip(destination: str, total_budget: float, nights: int = 1) -> str:
    """Plan a complete trip within a total budget.

    Args:
        destination: Name of the destination (case-insensitive)
        total_budget: Total trip budget in USD
        nights: Number of nights for accommodation (default 1)

    Finds combinations of hotel (price_per_night × nights) + restaurant + activity
    that fit within total_budget. Returns cost breakdown by category.
    If no complete plan fits, returns minimum budget required and suggests partial plans.
    """
    key = _normalize_destination(destination)

    if key not in DESTINATIONS:
        available = ", ".join(dest["name"] for dest in DESTINATIONS.values())
        return (
            f"Destination '{destination}' not found. "
            f"Available destinations are: {available}"
        )

    dest_name = DESTINATIONS[key]["name"]
    hotels = HOTELS.get(key, [])
    restaurants = RESTAURANTS.get(key, [])
    activities = ACTIVITIES.get(key, [])

    if not hotels or not restaurants or not activities:
        return (
            f"Insufficient data for {dest_name}. "
            f"Need hotels, restaurants, and activities to plan a complete trip."
        )

    # Calculate all possible combinations within budget
    valid_plans = []
    for hotel in hotels:
        accommodation_cost = hotel["price_per_night"] * nights
        for restaurant in restaurants:
            dining_cost = restaurant["price_range"]
            for activity in activities:
                activity_cost = activity["cost"]
                total_cost = accommodation_cost + dining_cost + activity_cost

                if total_cost <= total_budget:
                    valid_plans.append({
                        "hotel": hotel,
                        "restaurant": restaurant,
                        "activity": activity,
                        "accommodation_cost": accommodation_cost,
                        "dining_cost": dining_cost,
                        "activity_cost": activity_cost,
                        "total_cost": total_cost,
                        "budget_remaining": total_budget - total_cost,
                    })

    if valid_plans:
        # Sort by total cost (best value first)
        valid_plans.sort(key=lambda p: p["total_cost"])

        lines = [
            f"Trip Plans for {dest_name} ({nights} night{'s' if nights > 1 else ''}, "
            f"budget: ${total_budget}):\n"
        ]

        for i, plan in enumerate(valid_plans, 1):
            lines.append(f"Plan {i}:")
            lines.append(
                f"  Accommodation: {plan['hotel']['name']} - "
                f"${plan['accommodation_cost']} "
                f"(${plan['hotel']['price_per_night']}/night × {nights} night{'s' if nights > 1 else ''})"
            )
            lines.append(
                f"  Dining: {plan['restaurant']['name']} ({plan['restaurant']['cuisine_type']}) - "
                f"${plan['dining_cost']}"
            )
            lines.append(
                f"  Activity: {plan['activity']['name']} - "
                f"${plan['activity_cost']}"
            )
            lines.append(f"  Total Cost: ${plan['total_cost']}")
            lines.append(f"  Budget Remaining: ${plan['budget_remaining']}")
            lines.append("")

        lines.append(f"Found {len(valid_plans)} plan(s) within your budget.")
        return "\n".join(lines)

    # No complete plan fits - calculate minimum budget and suggest partial plans
    min_hotel_cost = min(h["price_per_night"] for h in hotels) * nights
    min_restaurant_cost = min(r["price_range"] for r in restaurants)
    min_activity_cost = min(a["cost"] for a in activities)
    min_budget_required = min_hotel_cost + min_restaurant_cost + min_activity_cost

    lines = [
        f"No complete trip plan fits within your budget of ${total_budget} "
        f"for {dest_name} ({nights} night{'s' if nights > 1 else ''}).\n"
    ]
    lines.append(f"Minimum budget required for a complete plan: ${min_budget_required}\n")

    # Suggest partial plans
    lines.append("Partial plans within your budget:\n")
    partial_found = False

    # Hotel + Activity combinations
    for hotel in hotels:
        accommodation_cost = hotel["price_per_night"] * nights
        for activity in activities:
            partial_cost = accommodation_cost + activity["cost"]
            if partial_cost <= total_budget:
                if not partial_found:
                    lines.append("  Hotel + Activity:")
                    partial_found = True
                lines.append(
                    f"    - {hotel['name']} + {activity['name']}: ${partial_cost}"
                )

    # Hotel + Restaurant combinations
    hotel_restaurant_found = False
    for hotel in hotels:
        accommodation_cost = hotel["price_per_night"] * nights
        for restaurant in restaurants:
            partial_cost = accommodation_cost + restaurant["price_range"]
            if partial_cost <= total_budget:
                if not hotel_restaurant_found:
                    lines.append("  Hotel + Restaurant:")
                    hotel_restaurant_found = True
                    partial_found = True
                lines.append(
                    f"    - {hotel['name']} + {restaurant['name']}: ${partial_cost}"
                )

    if not partial_found:
        lines.append(
            f"  No partial plans fit within ${total_budget} either.\n"
            f"  Cheapest hotel alone: ${min_hotel_cost} "
            f"({nights} night{'s' if nights > 1 else ''})"
        )

    return "\n".join(lines)
