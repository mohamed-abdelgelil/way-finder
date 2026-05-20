# destination_tool.py
# Destination discovery tool for the Egypt Travel Agent

from strands import tool
from travel_data import DESTINATIONS, HOTELS, RESTAURANTS, ACTIVITIES


def _normalize_destination(destination: str) -> str:
    """Normalize destination name for case-insensitive dictionary lookup."""
    return destination.strip().lower()


@tool
def get_destinations() -> str:
    """Get all available Egypt travel destinations.

    Returns a formatted list of all destination names and descriptions
    from the travel data.
    """
    if not DESTINATIONS:
        return "No destinations are currently available."

    lines = ["Available Egypt Destinations:\n"]
    for key, dest in DESTINATIONS.items():
        lines.append(f"- {dest['name']} ({dest['region']}): {dest['description']}")

    return "\n".join(lines)


@tool
def get_destination_details(destination: str) -> str:
    """Get detailed information about a specific Egypt destination.

    Args:
        destination: Name of the destination (case-insensitive)

    Returns detailed information including description, region,
    and a summary of available hotels, restaurants, and activities.
    """
    key = _normalize_destination(destination)

    if key not in DESTINATIONS:
        available = ", ".join(dest["name"] for dest in DESTINATIONS.values())
        return (
            f"Destination '{destination}' not found. "
            f"Available destinations are: {available}"
        )

    dest = DESTINATIONS[key]
    hotels = HOTELS.get(key, [])
    restaurants = RESTAURANTS.get(key, [])
    activities = ACTIVITIES.get(key, [])

    lines = [
        f"Destination: {dest['name']}",
        f"Region: {dest['region']}",
        f"Description: {dest['description']}",
        f"",
        f"Available options:",
        f"  Hotels: {len(hotels)} available",
        f"  Restaurants: {len(restaurants)} available",
        f"  Activities: {len(activities)} available",
    ]

    return "\n".join(lines)
