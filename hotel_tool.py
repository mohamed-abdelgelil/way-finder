# hotel_tool.py
# Hotel recommendation tool for the Egypt Travel Agent

from strands import tool
from travel_data import HOTELS, DESTINATIONS


def _normalize_destination(destination: str) -> str:
    """Normalize destination name for case-insensitive dictionary lookup."""
    return destination.strip().lower()


@tool
def get_hotels(destination: str, budget: float = None) -> str:
    """Get hotel recommendations for a destination, optionally filtered by budget.

    Args:
        destination: Name of the destination (case-insensitive)
        budget: Maximum price per night in USD (optional)

    Returns hotel name, price per night, and rating for each matching result.
    If budget is provided, only hotels with price_per_night <= budget are returned.
    If no hotels match the budget, suggests nearest available price options.
    """
    key = _normalize_destination(destination)

    if key not in HOTELS:
        available = ", ".join(dest["name"] for dest in DESTINATIONS.values())
        return (
            f"Destination '{destination}' not found. "
            f"Available destinations are: {available}"
        )

    hotels = HOTELS[key]

    if budget is not None and budget > 0:
        filtered = [h for h in hotels if h["price_per_night"] <= budget]

        if not filtered:
            # Suggest nearest available price options
            sorted_hotels = sorted(hotels, key=lambda h: h["price_per_night"])
            suggestions = []
            for h in sorted_hotels:
                suggestions.append(
                    f"  - {h['name']}: ${h['price_per_night']}/night (Rating: {h['rating']})"
                )
            return (
                f"No hotels in {DESTINATIONS[key]['name']} are available within "
                f"your budget of ${budget}/night.\n"
                f"Here are the nearest available options:\n"
                + "\n".join(suggestions)
            )

        hotels = filtered

    lines = [f"Hotels in {DESTINATIONS[key]['name']}:\n"]
    for h in hotels:
        lines.append(
            f"- {h['name']}: ${h['price_per_night']}/night (Rating: {h['rating']})"
        )

    return "\n".join(lines)
