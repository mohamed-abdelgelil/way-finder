# test_properties.py
# Property-based tests for the Egypt Travel Frontend API

import uuid
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient
from hypothesis import given, settings
from hypothesis import strategies as st

from app import app

client = TestClient(app)


# Strategy: valid message strings (1-2000 chars, not whitespace-only)
valid_message_strategy = st.text(
    min_size=1,
    max_size=2000,
    alphabet=st.characters(codec="utf-8", categories=("L", "N", "P", "S", "Z")),
).filter(lambda s: len(s.strip()) > 0)


# Feature: egypt-travel-frontend, Property 1: Valid request produces structured response
class TestProperty1ValidRequestResponseStructure:
    """
    Property 1: Valid request produces structured response

    For any valid message string (1-2000 non-whitespace-only characters),
    sending it to the POST /chat endpoint shall return an HTTP 200 response
    containing a JSON object with a non-empty "response" field and a valid
    "session_id" string field.

    **Validates: Requirements 1.1**
    """

    @given(message=valid_message_strategy)
    @settings(max_examples=100)
    @patch("app.session_store")
    def test_valid_message_returns_200_with_structured_response(self, mock_store, message):
        """For any valid message, the endpoint returns 200 with response and session_id."""
        # Mock the agent to return a predictable string response
        mock_result = MagicMock()
        mock_result.__str__ = MagicMock(return_value="Agent response for testing")
        mock_agent = MagicMock(return_value=mock_result)

        test_session_id = str(uuid.uuid4())
        mock_store.create_session.return_value = test_session_id
        mock_store.get_session.return_value = mock_agent

        response = client.post("/chat", json={"message": message})

        # Assert HTTP 200
        assert response.status_code == 200, (
            f"Expected 200 for message {message!r}, got {response.status_code}"
        )

        data = response.json()

        # Assert response contains non-empty "response" field
        assert "response" in data, f"Missing 'response' field in {data}"
        assert isinstance(data["response"], str), (
            f"Expected 'response' to be a string, got {type(data['response'])}"
        )
        assert len(data["response"]) > 0, "Expected non-empty 'response' field"

        # Assert response contains valid UUID "session_id" field
        assert "session_id" in data, f"Missing 'session_id' field in {data}"
        assert isinstance(data["session_id"], str), (
            f"Expected 'session_id' to be a string, got {type(data['session_id'])}"
        )
        # Validate that session_id is a valid UUID v4
        parsed_uuid = uuid.UUID(data["session_id"], version=4)
        assert str(parsed_uuid) == data["session_id"], (
            f"session_id '{data['session_id']}' is not a valid UUID v4"
        )


# Feature: egypt-travel-frontend, Property 2: Invalid input produces 400 error
class TestProperty2InvalidInputRejection:
    """
    Property 2: Invalid input produces 400 error

    For any request payload that is missing the "message" field, contains an
    empty "message" field, or contains a "message" field composed entirely of
    whitespace, the POST /chat endpoint shall return an HTTP 400 response with
    a JSON object containing an "error" string field.

    **Validates: Requirements 1.6**
    """

    @given(
        payload=st.one_of(
            # Dicts without "message" key
            st.fixed_dictionaries({"session_id": st.text(min_size=0, max_size=50)}),
            st.just({}),
            st.fixed_dictionaries({"other_field": st.text(min_size=0, max_size=50)}),
            # Dicts with empty "message"
            st.just({"message": ""}),
            # Dicts with whitespace-only "message"
            st.fixed_dictionaries(
                {"message": st.text(
                    alphabet=st.sampled_from([" ", "\t", "\n", "\r", "\f", "\v"]),
                    min_size=1,
                    max_size=100,
                )}
            ),
        )
    )
    @settings(max_examples=100)
    def test_invalid_input_returns_400_with_error_field(self, payload):
        """Any payload missing 'message', with empty 'message', or whitespace-only
        'message' must produce HTTP 400 with an 'error' field in the JSON response."""
        response = client.post("/chat", json=payload)

        assert response.status_code == 400, (
            f"Expected 400 for payload {payload!r}, got {response.status_code}"
        )

        data = response.json()
        assert "error" in data, (
            f"Expected 'error' field in response for payload {payload!r}, got {data}"
        )
        assert isinstance(data["error"], str), (
            f"Expected 'error' to be a string, got {type(data['error'])}"
        )
        assert len(data["error"]) > 0, (
            f"Expected non-empty 'error' string for payload {payload!r}"
        )


# The generic error message returned by the backend for agent errors
_GENERIC_ERROR_MSG = "The travel agent encountered an error. Please try again."


# Feature: egypt-travel-frontend, Property 3: Agent errors produce 500 response
class TestProperty3AgentErrorsProduceFiveHundred:
    """
    Property 3: Agent errors produce 500 response

    For any exception raised by the Agent during message processing,
    the POST /chat endpoint shall return an HTTP 500 response with a JSON
    object containing an "error" string field, and shall never expose the
    raw exception traceback to the client.

    **Validates: Requirements 1.5**
    """

    @given(
        error_message=st.text(min_size=1, max_size=200),
        exception_type=st.sampled_from([RuntimeError, ValueError, TypeError, Exception]),
    )
    @settings(max_examples=100)
    @patch("app.session_store")
    def test_agent_errors_produce_500_response(self, mock_store, error_message, exception_type):
        """Any exception raised by the agent produces a 500 with an error field
        and never exposes the traceback or raw error message to the client."""
        # Mock get_session: no session_id in request, so get_session is called
        # only once after create_session — return the mock agent that raises
        mock_agent = MagicMock(side_effect=exception_type(error_message))
        mock_store.get_session.return_value = mock_agent
        mock_store.create_session.return_value = "test-session-id"

        response = client.post("/chat", json={"message": "Hello"})

        # Assert HTTP 500
        assert response.status_code == 500

        # Assert "error" field exists in response JSON
        data = response.json()
        assert "error" in data
        assert isinstance(data["error"], str)

        # Assert the generated error message text does NOT appear in the response body.
        # We only check messages that wouldn't naturally appear as a substring of the
        # generic error response or the JSON envelope (short random strings like "r",
        # "e", or "{" trivially match JSON structure or the generic message).
        response_text = response.text
        if len(error_message) > 3 and error_message not in _GENERIC_ERROR_MSG:
            assert error_message not in response_text

        # Assert "Traceback" does NOT appear in the response body
        assert "Traceback" not in response_text


# Feature: egypt-travel-frontend, Property 4: Session creation for missing or invalid identifiers
class TestProperty4SessionCreationForInvalidIds:
    """
    Property 4: Session creation for missing or invalid identifiers

    For any request that either omits the session_id field or provides a session_id
    that does not correspond to an active session, the backend shall create a new
    session, return a unique UUID session_id in the response, and set the "new_session"
    field to true.

    **Validates: Requirements 2.3, 2.5**
    """

    @given(
        invalid_session_id=st.text(min_size=1, max_size=200).filter(
            lambda s: not _is_valid_uuid(s)
        )
    )
    @settings(max_examples=100)
    @patch("app.session_store")
    def test_invalid_session_id_creates_new_session(self, mock_store, invalid_session_id):
        """For any non-UUID string session_id (non-empty), the backend creates a new
        session with new_session=true and a valid UUID session_id."""
        new_uuid = str(uuid.uuid4())
        mock_agent = MagicMock()
        mock_result = MagicMock()
        mock_result.__str__ = MagicMock(return_value="Welcome to Egypt!")
        mock_agent.return_value = mock_result

        # App logic: if session_id is truthy, get_session is called first (returns None
        # for invalid ID), then create_session is called, then get_session again with new ID.
        mock_store.get_session.side_effect = [None, mock_agent]
        mock_store.create_session.return_value = new_uuid

        response = client.post(
            "/chat",
            json={"message": "Hello", "session_id": invalid_session_id},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["new_session"] is True
        assert _is_valid_uuid(data["session_id"])

    @given(
        message=st.text(min_size=1, max_size=100).filter(lambda s: len(s.strip()) > 0)
    )
    @settings(max_examples=100)
    @patch("app.session_store")
    def test_none_session_id_creates_new_session(self, mock_store, message):
        """For any valid message with session_id omitted (None), the backend creates
        a new session with new_session=true and a valid UUID session_id."""
        new_uuid = str(uuid.uuid4())
        mock_agent = MagicMock()
        mock_result = MagicMock()
        mock_result.__str__ = MagicMock(return_value="Agent response")
        mock_agent.return_value = mock_result

        # No session_id provided, so get_session won't be called with a valid ID
        mock_store.get_session.return_value = mock_agent
        mock_store.create_session.return_value = new_uuid

        response = client.post(
            "/chat",
            json={"message": message},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["new_session"] is True
        assert _is_valid_uuid(data["session_id"])


def _is_valid_uuid(value: str) -> bool:
    """Check if a string is a valid UUID."""
    try:
        uuid.UUID(str(value))
        return True
    except (ValueError, AttributeError):
        return False


# Feature: egypt-travel-frontend, Property 5: Session ID consistency
class TestProperty5SessionIDConsistency:
    """
    Property 5: Session ID consistency

    For any request that includes a valid, non-expired session_id, the response
    shall contain the same session_id value that was sent in the request.

    **Validates: Requirements 2.4**
    """

    @given(
        message=st.text(
            min_size=1,
            max_size=2000,
            alphabet=st.characters(blacklist_categories=("Cs",)),
        ).filter(lambda s: len(s.strip()) > 0)
    )
    @settings(max_examples=100)
    @patch("app.session_store")
    def test_response_session_id_matches_request_session_id(self, mock_store, message):
        """For any valid message sent with an existing session_id,
        the response session_id must equal the request session_id."""
        session_id = "valid-session-id-abc-123"

        # Mock get_session to return a mock agent for this session_id
        mock_result = MagicMock()
        mock_result.__str__ = MagicMock(return_value="Agent response")
        mock_agent = MagicMock(return_value=mock_result)
        mock_store.get_session.return_value = mock_agent

        response = client.post(
            "/chat",
            json={"message": message, "session_id": session_id},
        )

        # Assert HTTP 200
        assert response.status_code == 200, (
            f"Expected 200 for message {message!r}, got {response.status_code}"
        )

        data = response.json()

        # Assert response session_id equals the request session_id
        assert data["session_id"] == session_id, (
            f"Expected session_id '{session_id}', got '{data['session_id']}'"
        )

        # Assert new_session is false (existing session was reused)
        assert data["new_session"] is False, (
            f"Expected new_session=False, got {data['new_session']}"
        )
