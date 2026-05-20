# session_manager.py
# Session management for the Egypt Travel Agent web interface

import uuid
import time

from strands import Agent
from strands.models.bedrock import BedrockModel

SESSION_TTL_SECONDS = 1800  # 30 minutes

EGYPT_TRAVEL_SYSTEM_PROMPT = """
You are an expert Egypt travel assistant. Your role is to help travelers plan
their trips to Egypt by providing personalized recommendations for destinations,
hotels, restaurants, activities, and complete trip plans.

You specialize in:
- Helping users discover Egypt's top travel destinations
- Recommending hotels that match their budget and preferences
- Suggesting restaurants based on cuisine preferences and budget
- Finding activities and experiences at each destination
- Planning complete trips within a specified budget

When interacting with users:
- Be friendly, knowledgeable, and enthusiastic about Egypt travel
- Remember user preferences (destination, budget) throughout the conversation
- Proactively use your tools to provide specific, data-driven recommendations
- Break down costs clearly when presenting trip plans
- If a user's budget is too low, suggest alternatives or partial plans
"""


class SessionStore:
    """In-memory session store with TTL expiration."""

    def __init__(self):
        self._sessions: dict[str, dict] = {}
        # Each entry: {"agent": Agent, "last_access": float}

    def create_session(self) -> str:
        """Create a new session with a fresh Agent instance.

        Returns:
            A unique session ID (UUID4 string).
        """
        session_id = str(uuid.uuid4())
        agent = self._create_agent()
        self._sessions[session_id] = {
            "agent": agent,
            "last_access": time.time(),
        }
        return session_id

    def get_session(self, session_id: str) -> Agent | None:
        """Get the Agent for a session, or None if expired/invalid.

        Updates the last_access timestamp on successful retrieval.

        Args:
            session_id: The session identifier to look up.

        Returns:
            The Agent instance if the session exists and is not expired,
            otherwise None.
        """
        entry = self._sessions.get(session_id)
        if entry is None:
            return None
        if time.time() - entry["last_access"] > SESSION_TTL_SECONDS:
            del self._sessions[session_id]
            return None
        entry["last_access"] = time.time()
        return entry["agent"]

    def cleanup_expired(self):
        """Remove all expired sessions."""
        now = time.time()
        expired = [
            sid for sid, entry in self._sessions.items()
            if now - entry["last_access"] > SESSION_TTL_SECONDS
        ]
        for sid in expired:
            del self._sessions[sid]

    def _create_agent(self) -> Agent:
        """Create a new Agent with the same config as the notebook."""
        from destination_tool import get_destinations, get_destination_details
        from hotel_tool import get_hotels
        from restaurant_tool import get_restaurants
        from activity_tool import get_activities
        from trip_planner_tool import plan_trip

        model = BedrockModel(
            model_id="anthropic.claude-sonnet-4-6",
            region_name="us-west-2",
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
