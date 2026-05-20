# test_session_manager.py
# Unit tests for the SessionStore class in session_manager.py

import sys
import unittest
from unittest.mock import patch, MagicMock
import uuid

# Mock the strands module and its submodules before importing session_manager
mock_strands = MagicMock()
mock_strands_models = MagicMock()
mock_strands_models_bedrock = MagicMock()

sys.modules["strands"] = mock_strands
sys.modules["strands.models"] = mock_strands_models
sys.modules["strands.models.bedrock"] = mock_strands_models_bedrock

# Now we can safely import session_manager
from session_manager import SessionStore  # noqa: E402


class TestSessionStore(unittest.TestCase):
    """Tests for SessionStore session management logic."""

    def setUp(self):
        """Create a SessionStore with mocked agent creation."""
        # Patch _create_agent so we never call real Agent/BedrockModel
        patcher = patch.object(
            SessionStore,
            "_create_agent",
            return_value=MagicMock(name="MockAgent"),
        )
        self.mock_create_agent = patcher.start()
        self.addCleanup(patcher.stop)

        self.store = SessionStore()

    def test_create_session_returns_valid_uuid(self):
        """create_session() returns a valid UUID4 string."""
        session_id = self.store.create_session()
        # Should not raise if it's a valid UUID
        parsed = uuid.UUID(session_id, version=4)
        self.assertEqual(str(parsed), session_id)

    def test_get_session_returns_agent_for_valid_session(self):
        """get_session() returns the Agent instance for a valid, non-expired session."""
        session_id = self.store.create_session()
        agent = self.store.get_session(session_id)
        self.assertIsNotNone(agent)
        # Should be the mock agent returned by _create_agent
        self.assertEqual(agent, self.mock_create_agent.return_value)

    def test_get_session_returns_none_for_invalid_id(self):
        """get_session() returns None for a session ID that doesn't exist."""
        result = self.store.get_session("nonexistent-session-id")
        self.assertIsNone(result)

    @patch("session_manager.time.time")
    def test_get_session_returns_none_for_expired_session(self, mock_time):
        """get_session() returns None when the session has expired (>30 min idle)."""
        # Time at session creation
        mock_time.return_value = 1000.0
        session_id = self.store.create_session()

        # Advance time past the 30-minute TTL (1800 seconds)
        mock_time.return_value = 1000.0 + 1801.0
        result = self.store.get_session(session_id)
        self.assertIsNone(result)

    @patch("session_manager.time.time")
    def test_cleanup_expired_removes_only_expired_sessions(self, mock_time):
        """cleanup_expired() removes expired sessions and keeps active ones."""
        # Create two sessions at t=1000
        mock_time.return_value = 1000.0
        session_active = self.store.create_session()
        session_expired = self.store.create_session()

        # Access the "active" session at t=2500 (refreshes its last_access)
        mock_time.return_value = 2500.0
        self.store.get_session(session_active)

        # Now at t=2900 — expired session was last accessed at t=1000 (1900s ago > 1800s TTL)
        # Active session was last accessed at t=2500 (400s ago < 1800s TTL)
        mock_time.return_value = 2900.0
        self.store.cleanup_expired()

        # Active session should still be accessible
        self.assertIsNotNone(self.store.get_session(session_active))
        # Expired session should be gone
        self.assertIsNone(self.store.get_session(session_expired))


if __name__ == "__main__":
    unittest.main()
