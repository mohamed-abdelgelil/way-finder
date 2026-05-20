"""
Agent session management.
Each session_id gets its own Agent instance so conversation memory is isolated per user.

Model: qwen2.5:3b via Ollama (local, no API key required)
       Uses Strands' native OllamaModel provider.
"""

import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from strands import Agent
from strands.models.ollama import OllamaModel

from destination_tool import get_destinations, get_destination_details
from hotel_tool import get_hotels
from restaurant_tool import get_restaurants
from activity_tool import get_activities
from trip_planner_tool import plan_trip

EGYPT_TRAVEL_SYSTEM_PROMPT = """You are an expert Egypt travel assistant. Help travelers plan trips to Egypt.

You have access to tools for:
- Listing available destinations
- Getting destination details
- Finding hotels (optionally filtered by budget)
- Finding restaurants (optionally filtered by cuisine and budget)
- Finding activities (optionally filtered by budget)
- Planning complete trips within a total budget

Always use your tools to get real data. Be concise and friendly.
When presenting trip plans or lists, use clear formatting.
"""

# In-memory session store: session_id -> Agent instance
_sessions: dict[str, Agent] = {}


def _create_agent() -> Agent:
    model = OllamaModel(
        host="http://localhost:11434",
        model_id="qwen2.5:3b",
        temperature=0.3,
    )
    return Agent(
        model=model,
        tools=[
            get_destinations,
            get_destination_details,
            get_hotels,
            get_restaurants,
            get_activities,
            plan_trip,
        ],
        system_prompt=EGYPT_TRAVEL_SYSTEM_PROMPT,
    )


def get_or_create_agent(session_id: str) -> Agent:
    if session_id not in _sessions:
        _sessions[session_id] = _create_agent()
    return _sessions[session_id]


def clear_session(session_id: str) -> None:
    _sessions.pop(session_id, None)
