# activity_tool.py
# Activity recommendations tool for the Egypt Travel Agent

from strands import tool
from travel_data import ACTIVITIES, DESTINATIONS


def _normalize_destination(destination: str) -> str:
    """Normalize destination name for case-insensitive dictionary lookup."""
    return destination.strip().lower()


@tool
def get_activities(destination: str, budget: float = None) -> str:
    """Get activity recommendations for a destination, optionally filtered by budget.

    Args:
        destination: Name of the destination (case-insensitive)
        budget: Maximum activity cost in USD (optional)

    Returns activity name, description, and cost for each matching result.
    When a budget is provided, only activities with cost <= budget are returned.
    If no activities match the budget, suggests nearest available cost options.
    """
    key = _normalize_destination(destination)

    if key not in DESTINATIONS:
        available = ", ".join(dest["name"] for dest in DESTINATIONS.values())
        return (
            f"Destination '{destination}' not found. "
            f"Available destinations are: {available}"
        )

    activities = ACTIVITIES.get(key, [])

    if not activities:
        return f"No activities are currently available for {DESTINATIONS[key]['name']}."

    # Apply budget filter if provided
    if budget is not None:
        filtered = [a for a in activities if a["cost"] <= budget]

        if not filtered:
            # Suggest nearest available cost options
            sorted_by_cost = sorted(activities, key=lambda a: a["cost"])
            suggestions = sorted_by_cost[:3]  # Suggest up to 3 nearest options
            lines = [
                f"No activities in {DESTINATIONS[key]['name']} are available within your budget of ${budget:.2f}.",
                "",
                "Nearest available options:",
            ]
            for activity in suggestions:
                lines.append(
                    f"- {activity['name']}: {activity['description']} (Cost: ${activity['cost']:.2f})"
                )
            return "\n".join(lines)

        activities = filtered

    # Format results
    dest_name = DESTINATIONS[key]["name"]
    lines = [f"Activities in {dest_name}:\n"]
    for activity in activities:
        lines.append(
            f"- {activity['name']}: {activity['description']} (Cost: ${activity['cost']:.2f})"
        )

    return "\n".join(lines)
