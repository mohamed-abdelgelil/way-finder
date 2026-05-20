"""
Intent-based router that maps user messages to tool calls.

This replaces the LLM agent for environments where a capable LLM is not
available. It uses keyword/pattern matching to detect intent and calls the
appropriate tool functions directly, maintaining a simple conversation state.

When a real LLM is available (Bedrock, Anthropic API, etc.) this module
can be swapped out for agent_session.py with no changes to main.py.
"""

import re
import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from destination_tool import get_destinations, get_destination_details
from hotel_tool import get_hotels
from restaurant_tool import get_restaurants
from activity_tool import get_activities
from trip_planner_tool import plan_trip

VALID_DESTINATIONS = ["cairo", "luxor", "aswan", "alexandria", "hurghada"]

HELP_TEXT = """I can help you with:
- **Destinations** — "What destinations are available?" or "Tell me about Cairo"
- **Hotels** — "Find hotels in Luxor" or "Hotels in Cairo under $100"
- **Restaurants** — "Restaurants in Aswan" or "Egyptian food in Cairo"
- **Activities** — "Activities in Hurghada" or "Things to do in Luxor under $50"
- **Trip planning** — "Plan a trip to Aswan with a budget of $300 for 2 nights"

Try one of the suggestions below to get started!"""


class ConversationSession:
    """Holds per-session state: last mentioned destination and budget."""

    def __init__(self):
        self.last_destination: str | None = None
        self.last_budget: float | None = None

    def update(self, destination: str | None = None, budget: float | None = None):
        if destination:
            self.last_destination = destination
        if budget is not None:
            self.last_budget = budget


# In-memory sessions
_sessions: dict[str, ConversationSession] = {}


def get_or_create_session(session_id: str) -> ConversationSession:
    if session_id not in _sessions:
        _sessions[session_id] = ConversationSession()
    return _sessions[session_id]


def clear_session(session_id: str) -> None:
    _sessions.pop(session_id, None)


# ── Extraction helpers ────────────────────────────────────────────────────────

def _extract_destination(text: str) -> str | None:
    t = text.lower()
    for dest in VALID_DESTINATIONS:
        if dest in t:
            return dest
    return None


def _extract_budget(text: str) -> float | None:
    # Match patterns like $200, 200 dollars, budget of 150, under 100
    patterns = [
        r'\$\s*(\d+(?:\.\d+)?)',
        r'(\d+(?:\.\d+)?)\s*(?:dollars?|usd)',
        r'budget\s+(?:of\s+)?(\d+(?:\.\d+)?)',
        r'under\s+\$?\s*(\d+(?:\.\d+)?)',
        r'within\s+\$?\s*(\d+(?:\.\d+)?)',
        r'(\d+(?:\.\d+)?)\s*(?:per night|/night)',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return float(m.group(1))
    return None


def _extract_nights(text: str) -> int:
    m = re.search(r'(\d+)\s*nights?', text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return 1


def _extract_cuisine(text: str) -> str | None:
    cuisines = ["egyptian", "mediterranean", "seafood", "nubian", "international",
                "middle eastern", "greek", "street food"]
    t = text.lower()
    for c in cuisines:
        if c in t:
            return c
    return None


# ── Intent detection ──────────────────────────────────────────────────────────

def _is_greeting(text: str) -> bool:
    t = text.lower().strip()
    return bool(re.match(r'^(hi|hello|hey|howdy|greetings|good\s*(morning|afternoon|evening))[!.,]?$', t))


def _intent(text: str) -> str:
    t = text.lower()

    # Trip planning — check first (most specific)
    if any(w in t for w in ["plan", "trip", "plan a trip", "plan my trip", "full trip", "complete trip"]):
        return "plan_trip"

    # Destination detail
    if any(w in t for w in ["tell me about", "describe", "what is", "info about", "details about", "about"]):
        dest = _extract_destination(t)
        if dest:
            return "destination_detail"

    # List destinations
    if any(w in t for w in ["destinations", "places", "cities", "where can i go", "what destinations",
                              "available destinations", "list destinations"]):
        return "list_destinations"

    # Hotels
    if any(w in t for w in ["hotel", "hotels", "stay", "accommodation", "where to stay", "lodge", "inn"]):
        return "hotels"

    # Restaurants
    if any(w in t for w in ["restaurant", "restaurants", "eat", "food", "dining", "cuisine", "where to eat"]):
        return "restaurants"

    # Activities
    if any(w in t for w in ["activit", "things to do", "what to do", "experience", "tour", "visit",
                              "attraction", "sightseeing", "excursion"]):
        return "activities"

    # Destination detail fallback — if a destination is mentioned alone
    dest = _extract_destination(t)
    if dest:
        return "destination_detail"

    return "unknown"


# ── Main dispatch ─────────────────────────────────────────────────────────────

def process_message(session_id: str, message: str) -> str:
    session = get_or_create_session(session_id)
    text = message.strip()

    # Greeting
    if _is_greeting(text):
        return ("👋 Welcome to the Egypt Travel Assistant!\n\n" + HELP_TEXT)

    intent = _intent(text)
    dest = _extract_destination(text) or session.last_destination
    budget = _extract_budget(text)
    if budget is None:
        budget = session.last_budget

    session.update(destination=dest, budget=budget)

    # ── List destinations ──────────────────────────────────────────────────
    if intent == "list_destinations":
        return get_destinations()

    # ── Destination detail ─────────────────────────────────────────────────
    if intent == "destination_detail":
        if not dest:
            return ("Which destination would you like to know about?\n\n"
                    "Available: Cairo, Luxor, Aswan, Alexandria, Hurghada")
        return get_destination_details(dest)

    # ── Hotels ────────────────────────────────────────────────────────────
    if intent == "hotels":
        if not dest:
            return ("Which destination are you looking for hotels in?\n\n"
                    "Available: Cairo, Luxor, Aswan, Alexandria, Hurghada")
        return get_hotels(dest, budget=budget)

    # ── Restaurants ───────────────────────────────────────────────────────
    if intent == "restaurants":
        if not dest:
            return ("Which destination are you looking for restaurants in?\n\n"
                    "Available: Cairo, Luxor, Aswan, Alexandria, Hurghada")
        cuisine = _extract_cuisine(text)
        return get_restaurants(dest, cuisine=cuisine, budget=budget)

    # ── Activities ────────────────────────────────────────────────────────
    if intent == "activities":
        if not dest:
            return ("Which destination are you looking for activities in?\n\n"
                    "Available: Cairo, Luxor, Aswan, Alexandria, Hurghada")
        return get_activities(dest, budget=budget)

    # ── Trip planning ─────────────────────────────────────────────────────
    if intent == "plan_trip":
        if not dest:
            return ("Which destination would you like to plan a trip to?\n\n"
                    "Available: Cairo, Luxor, Aswan, Alexandria, Hurghada")
        if not budget:
            return (f"What's your total budget for the trip to {dest.title()}? "
                    f"(e.g. \"$300\" or \"500 dollars\")")
        nights = _extract_nights(text)
        if nights == 1 and session.last_destination == dest:
            # Try to extract nights from context
            nights = _extract_nights(message)
        return plan_trip(dest, total_budget=budget, nights=nights)

    # ── Unknown ───────────────────────────────────────────────────────────
    # Try to be helpful based on what we can extract
    if dest:
        return (f"I can help you with information about **{dest.title()}**. What would you like to know?\n\n"
                f"- Hotels in {dest.title()}\n"
                f"- Restaurants in {dest.title()}\n"
                f"- Activities in {dest.title()}\n"
                f"- Plan a trip to {dest.title()}")

    return ("I'm not sure what you're looking for. Here's what I can help with:\n\n" + HELP_TEXT)
