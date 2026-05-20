# Implementation Plan: Egypt Travel Frontend

## Overview

Build a chat-style web interface for the Egypt Travel Agent. The implementation creates a FastAPI backend (`app.py`) with session management (`session_manager.py`) that wraps the existing Strands Agent, and a vanilla HTML/CSS/JS frontend (`static/index.html`) that communicates with the backend via a single POST /chat endpoint. Tasks are ordered so that the backend is functional before the frontend is wired up, enabling incremental testing.

## Tasks

- [ ] 1. Set up backend project structure and dependencies
  - [x] 1.1 Create the session manager module
    - Create `session_manager.py` with the `SessionStore` class
    - Implement `create_session()` that instantiates a Strands Agent with BedrockModel (model_id="anthropic.claude-sonnet-4-6", region_name="us-west-2") and the existing tools (get_destinations, get_destination_details, get_hotels, get_restaurants, get_activities, plan_trip)
    - Implement `get_session(session_id)` that returns the Agent if the session exists and is not expired, otherwise returns None
    - Implement `cleanup_expired()` that removes sessions older than 30 minutes
    - Define `SESSION_TTL_SECONDS = 1800` (30 minutes)
    - Include the Egypt travel system prompt matching the notebook's agent configuration
    - _Requirements: 2.1, 2.2, 2.3, 2.5, 2.6_

  - [-] 1.2 Create the FastAPI application with POST /chat endpoint
    - Create `app.py` with FastAPI app, CORS middleware (allow all origins), and Pydantic models (ChatRequest, ChatResponse, ErrorResponse)
    - Implement `POST /chat` endpoint that validates the request, looks up or creates a session, calls the agent with asyncio.wait_for (60s timeout), and returns the response
    - Return HTTP 400 for missing/empty/whitespace-only message or message exceeding 2000 characters
    - Return HTTP 500 with generic error message when the agent raises an exception (never expose tracebacks)
    - Return HTTP 504 when the agent call exceeds 60 seconds
    - When session_id is missing or invalid/expired, create a new session and set `new_session: true` in the response
    - When session_id is valid, echo it back in the response with `new_session: false`
    - Mount static files directory and serve `static/index.html` at the root route
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 2.2, 2.3, 2.4, 2.5_

- [~] 2. Checkpoint - Verify backend
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 3. Implement the chat frontend
  - [~] 3.1 Create the HTML structure and CSS styles
    - Create `static/index.html` with the chat container, chat header ("Egypt Travel Agent"), chat window, and input area (text input + character count + send button)
    - Style user messages right-aligned with a distinct background color, agent messages left-aligned with a different background color, and error messages with a red/warning background color
    - Add responsive CSS: full-width layout below 768px viewport, centered max-width 800px layout at 768px and above
    - Ensure minimum 16px font size for message text on all screen sizes
    - Ensure minimum 44x44px tap targets for send button and input on mobile viewports
    - Display a timestamp alongside each message
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 6.1, 6.2, 6.3, 6.4_

  - [~] 3.2 Implement JavaScript chat logic
    - Implement session ID management using `localStorage` (store and retrieve session_id)
    - Implement `sendMessage()`: validate input (non-empty, non-whitespace, ≤2000 chars), display user message optimistically, clear input, disable input/button, show loading indicator, send POST /chat with message and session_id, handle response
    - Implement message rendering: append message elements to chat window with role-based styling (user/agent/error/welcome), include formatted timestamp, auto-scroll to bottom
    - Implement send triggers: click send button or press Enter (without Shift)
    - Implement input validation: disable send button when input is empty/whitespace-only, show character count, prevent submission when exceeding 2000 characters with a visual limit indicator
    - Implement loading indicator: show a typing/loading element in the chat window while waiting for response
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_

  - [~] 3.3 Implement error handling and welcome experience
    - Handle API error responses (4xx/5xx): display error message in chat window with distinct styling, remove loading indicator, re-enable input
    - Handle network errors (fetch failure): display "Unable to connect to the server. Check your connection." in chat window
    - Handle timeout (30s client-side): use AbortController, abort fetch after 30 seconds, display timeout error message
    - On any error: preserve the user's most recent message in the chat window
    - Implement welcome message: on page load, if no session_id in localStorage, display a welcome message from the agent mentioning destinations, hotels, restaurants, activities, and trip planning in Egypt
    - If session_id exists in localStorage, skip the welcome message
    - Retain welcome message in chat history after first user message
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 7.1, 7.2, 7.3, 7.4, 7.5_

- [~] 4. Checkpoint - Verify frontend integration
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Backend unit tests
  - [~] 5.1 Write unit tests for session manager
    - Create `test_session_manager.py` using unittest
    - Test `create_session()` returns a valid UUID string
    - Test `get_session()` returns an Agent for a valid session
    - Test `get_session()` returns None for an invalid session ID
    - Test session expiration: mock time to advance past 30 minutes, verify `get_session()` returns None
    - Test `cleanup_expired()` removes only expired sessions
    - _Requirements: 2.1, 2.3, 2.5, 2.6_

  - [~] 5.2 Write unit tests for the /chat endpoint
    - Create `test_app.py` using unittest and FastAPI's TestClient
    - Test valid message returns 200 with response and session_id fields
    - Test missing message field returns 400
    - Test empty message returns 400
    - Test whitespace-only message returns 400
    - Test message exceeding 2000 characters returns 400
    - Test agent exception returns 500 with error field (no traceback)
    - Test agent timeout returns 504
    - Test new session creation when session_id is omitted (new_session: true)
    - Test existing session reuse when valid session_id is provided (same session_id echoed)
    - Test invalid session_id creates new session (new_session: true)
    - Test CORS headers are present in response
    - _Requirements: 1.1, 1.4, 1.5, 1.6, 1.7, 2.3, 2.4, 2.5_

- [~] 6. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Property-based tests
  - [ ]* 7.1 Write property test for valid request response structure (Property 1)
    - **Property 1: Valid request produces structured response**
    - Use hypothesis to generate random valid strings (1-2000 chars, non-whitespace-only)
    - Mock the Agent to return a string response
    - Assert HTTP 200, response contains non-empty "response" field and valid UUID "session_id" field
    - **Validates: Requirements 1.1**

  - [ ]* 7.2 Write property test for invalid input rejection (Property 2)
    - **Property 2: Invalid input produces 400 error**
    - Use hypothesis to generate payloads with missing "message", empty "message", or whitespace-only "message"
    - Assert HTTP 400 with "error" field in response
    - **Validates: Requirements 1.6**

  - [ ]* 7.3 Write property test for agent error handling (Property 3)
    - **Property 3: Agent errors produce 500 response**
    - Use hypothesis to generate random exception types and messages
    - Mock the Agent to raise the generated exception
    - Assert HTTP 500 with "error" field, assert traceback text is NOT in response body
    - **Validates: Requirements 1.5**

  - [ ]* 7.4 Write property test for session creation on missing/invalid IDs (Property 4)
    - **Property 4: Session creation for missing or invalid identifiers**
    - Use hypothesis to generate random non-UUID strings and None values for session_id
    - Assert response contains a valid UUID session_id and new_session is true
    - **Validates: Requirements 2.3, 2.5**

  - [ ]* 7.5 Write property test for session ID consistency (Property 5)
    - **Property 5: Session ID consistency**
    - Create a session, then use hypothesis to generate random messages sent with that session_id
    - Assert response session_id matches the request session_id
    - **Validates: Requirements 2.4**

  - [ ]* 7.6 Write property test for session isolation (Property 6)
    - **Property 6: Session isolation**
    - Create two sessions, send random messages to each
    - Assert that messages to one session do not appear in the other session's history
    - **Validates: Requirements 2.1, 2.2**

- [~] 8. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- The backend must be functional before the frontend can be tested end-to-end
- All code uses Python 3.11+ (backend) and vanilla JS (frontend) — no build step required
- FastAPI serves static files directly; no separate web server needed for development

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2"] },
    { "id": 2, "tasks": ["3.1"] },
    { "id": 3, "tasks": ["3.2"] },
    { "id": 4, "tasks": ["3.3"] },
    { "id": 5, "tasks": ["5.1", "5.2"] },
    { "id": 6, "tasks": ["7.1", "7.2", "7.3", "7.4", "7.5", "7.6"] }
  ]
}
```
