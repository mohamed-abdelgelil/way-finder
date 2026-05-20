# restaurant_tool.py
# Restaurant recommendation tool for the Egypt Travel Agent

from strands import tool
from travel_data import DESTINATIONS, RESTAURANTS


def _normalize_destination(destination: str) -> str:
    """Normalize destination name for case-insensitive dictionary lookup."""
    return destination.strip().lower()


@tool
def get_restaurants(destination: str, cuisine: str = None, budget: float = None) -> str:
    """Get restaurant recommendations for a destination.

    Args:
        destination: Name of the destination (case-insensitive)
        cuisine: Preferred cuisine type (optional, case-insensitive match)
        budget: Maximum price per meal in USD (optional)

    Returns restaurant name, cuisine type, and price range for each
    matching result. Filters by cuisine and/or budget when provided.
    """
    key = _normalize_destination(destination)

    if key not in DESTINATIONS:
        available = ", ".join(dest["name"] for dest in DESTINATIONS.values())
        return (
            f"Destination '{destination}' not found. "
            f"Available destinations are: {available}"
        )

    restaurants = RESTAURANTS.get(key, [])

    if not restaurants:
        return f"No restaurants are currently available for {DESTINATIONS[key]['name']}."

    filtered = restaurants

    # Filter by cuisine type (case-insensitive)
    if cuisine:
        filtered = [
            r for r in filtered
            if r["cuisine_type"].lower() == cuisine.strip().lower()
        ]

    # Filter by budget (price_range <= budget)
    if budget is not None:
        filtered = [r for r in filtered if r["price_range"] <= budget]

    if not filtered:
        # No matches — list available cuisine types to help the user
        available_cuisines = sorted(set(r["cuisine_type"] for r in restaurants))
        cuisine_list = ", ".join(available_cuisines)
        return (
            f"No restaurants match your criteria in {DESTINATIONS[key]['name']}. "
            f"Available cuisine types: {cuisine_list}"
        )

    # Format results
    dest_name = DESTINATIONS[key]["name"]
    lines = [f"Restaurants in {dest_name}:\n"]
    for r in filtered:
        lines.append(
            f"- {r['name']} | Cuisine: {r['cuisine_type']} | "
            f"Price: ${r['price_range']}/meal"
        )

    return "\n".join(lines)
