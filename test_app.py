# test_app.py
# Unit tests for the /chat endpoint

import asyncio
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app import app


class TestChatEndpoint(unittest.TestCase):
    """Unit tests for POST /chat endpoint."""

    def setUp(self):
        self.client = TestClient(app)

    # --- Mock helper ---

    def _mock_agent_response(self, text="Hello from the agent!"):
        """Create a mock agent callable that returns a result with str() support."""
        mock_result = MagicMock()
        mock_result.__str__ = MagicMock(return_value=text)
        mock_agent = MagicMock(return_value=mock_result)
        return mock_agent

    # --- Valid request tests ---

    @patch("app.session_store")
    def test_valid_message_returns_200_with_response_and_session_id(self, mock_store):
        """Test that a valid message returns 200 with response and session_id fields."""
        mock_agent = self._mock_agent_response("I can help with Egypt travel!")
        mock_store.create_session.return_value = "test-session-id-123"
        # No session_id provided, so get_session is only called after create_session
        mock_store.get_session.return_value = mock_agent

        response = self.client.post("/chat", json={"message": "Hello"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("response", data)
        self.assertIn("session_id", data)
        self.assertEqual(data["session_id"], "test-session-id-123")
        self.assertIsInstance(data["response"], str)
        self.assertTrue(len(data["response"]) > 0)

    # --- Validation error tests ---

    def test_missing_message_field_returns_400(self):
        """Test that a request without a message field returns 400."""
        response = self.client.post("/chat", json={"session_id": "abc"})

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)

    def test_empty_message_returns_400(self):
        """Test that an empty message returns 400."""
        response = self.client.post("/chat", json={"message": ""})

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)

    def test_whitespace_only_message_returns_400(self):
        """Test that a whitespace-only message returns 400."""
        response = self.client.post("/chat", json={"message": "   \t\n  "})

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)

    def test_message_exceeding_2000_chars_returns_400(self):
        """Test that a message exceeding 2000 characters returns 400."""
        long_message = "a" * 2001
        response = self.client.post("/chat", json={"message": long_message})

        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("error", data)

    # --- Agent error tests ---

    @patch("app.session_store")
    def test_agent_exception_returns_500_with_error_field(self, mock_store):
        """Test that an agent exception returns 500 with error field and no traceback."""
        mock_agent = MagicMock(side_effect=RuntimeError("Internal bedrock failure"))
        mock_store.create_session.return_value = "test-session-id"
        mock_store.get_session.return_value = mock_agent

        response = self.client.post("/chat", json={"message": "Hello"})

        self.assertEqual(response.status_code, 500)
        data = response.json()
        self.assertIn("error", data)
        # Should not expose traceback details
        self.assertNotIn("Traceback", data["error"])
        self.assertNotIn("RuntimeError", data["error"])
        self.assertNotIn("Internal bedrock failure", data["error"])

    @patch("app.asyncio.wait_for")
    @patch("app.session_store")
    def test_agent_timeout_returns_504(self, mock_store, mock_wait_for):
        """Test that an agent timeout returns 504."""
        mock_agent = self._mock_agent_response()
        mock_store.create_session.return_value = "test-session-id"
        mock_store.get_session.return_value = mock_agent
        mock_wait_for.side_effect = asyncio.TimeoutError()

        response = self.client.post("/chat", json={"message": "Plan my trip"})

        self.assertEqual(response.status_code, 504)
        data = response.json()
        self.assertIn("error", data)

    # --- Session management tests ---

    @patch("app.session_store")
    def test_new_session_created_when_session_id_omitted(self, mock_store):
        """Test that omitting session_id creates a new session (new_session: true)."""
        mock_agent = self._mock_agent_response("Welcome!")
        mock_store.create_session.return_value = "new-session-uuid"
        mock_store.get_session.return_value = mock_agent

        response = self.client.post("/chat", json={"message": "Hi"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["session_id"], "new-session-uuid")
        self.assertTrue(data["new_session"])

    @patch("app.session_store")
    def test_existing_session_reuse_echoes_session_id(self, mock_store):
        """Test that providing a valid session_id echoes it back (same session reused)."""
        mock_agent = self._mock_agent_response("I remember you!")
        mock_store.get_session.return_value = mock_agent

        response = self.client.post(
            "/chat", json={"message": "Hello again", "session_id": "existing-session-123"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["session_id"], "existing-session-123")
        self.assertFalse(data["new_session"])

    @patch("app.session_store")
    def test_invalid_session_id_creates_new_session(self, mock_store):
        """Test that an invalid session_id creates a new session (new_session: true)."""
        mock_agent = self._mock_agent_response("Starting fresh!")
        # First call with the invalid ID returns None, second call after create returns agent
        mock_store.get_session.side_effect = [None, mock_agent]
        mock_store.create_session.return_value = "brand-new-session-id"

        response = self.client.post(
            "/chat", json={"message": "Hi", "session_id": "invalid-nonexistent-id"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["session_id"], "brand-new-session-id")
        self.assertTrue(data["new_session"])
        # Verify create_session was called since the original session was invalid
        mock_store.create_session.assert_called_once()

    # --- CORS tests ---

    def test_cors_headers_present_in_response(self):
        """Test that CORS headers are present in response."""
        response = self.client.options(
            "/chat",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )

        # CORS preflight should return 200
        self.assertEqual(response.status_code, 200)
        self.assertIn("access-control-allow-origin", response.headers)
        self.assertEqual(response.headers["access-control-allow-origin"], "*")


if __name__ == "__main__":
    unittest.main()
