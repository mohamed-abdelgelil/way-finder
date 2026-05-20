# Requirements Document

## Introduction

This document specifies the requirements for a web-based frontend and backend API layer for the Egypt Travel Agent. The existing agent runs as a Jupyter notebook conversation loop using the Strands Agents SDK with Amazon Bedrock. This feature adds a chat-style web interface that allows users to interact with the agent through a browser, backed by a REST API that wraps the existing agent logic. The system preserves the agent's session memory, tool capabilities, and conversational behavior while making it accessible over HTTP.

## Glossary

- **Frontend**: A browser-based single-page application providing a chat interface for users to interact with the Egypt Travel Agent
- **Backend_API**: A Python web server that exposes the Egypt Travel Agent as an HTTP endpoint, managing agent sessions and forwarding user messages to the Strands Agent
- **Chat_Message**: A single message in the conversation, containing text content, a sender role (user or agent), and a timestamp
- **Session**: A server-side conversation context that maintains the Strands Agent instance and its conversation history for a connected user
- **Chat_Window**: The scrollable area in the Frontend that displays the conversation history between the user and the agent
- **Message_Input**: The text input field and send button in the Frontend where users compose and submit messages
- **Agent**: The existing Strands Agents SDK-based conversational AI assistant configured with Egypt travel tools and Amazon Bedrock
- **Loading_Indicator**: A visual element displayed in the Frontend while the Backend_API is processing a user message

## Requirements

### Requirement 1: Backend API Server

**User Story:** As a developer, I want a Python web server that wraps the existing agent, so that the frontend can communicate with the agent over HTTP.

#### Acceptance Criteria

1. THE Backend_API SHALL expose a POST endpoint that accepts a JSON payload containing a "message" text field (maximum 2000 characters) and returns a JSON payload containing a "response" text field with the agent's reply
2. THE Backend_API SHALL instantiate the Strands Agent with the same configuration as the existing notebook (same tools, system prompt, and Bedrock model)
3. WHEN a message is received on the POST endpoint, THE Backend_API SHALL forward the message to the Agent and return the agent's text response within 60 seconds
4. THE Backend_API SHALL enable CORS to allow requests from all origins during development
5. IF the Agent raises an error during processing, THEN THE Backend_API SHALL return an HTTP 500 response with a JSON payload containing an "error" field that indicates the nature of the failure
6. IF the POST request body is missing, not valid JSON, or does not contain a non-empty "message" field, THEN THE Backend_API SHALL return an HTTP 400 response with a JSON payload containing an "error" field indicating the validation failure
7. IF the Agent does not return a response within 60 seconds, THEN THE Backend_API SHALL abort the request and return an HTTP 504 response with a JSON payload containing an "error" field indicating a timeout occurred

### Requirement 2: Session Management

**User Story:** As a user, I want the agent to remember my conversation context, so that I can have a multi-turn conversation without repeating myself.

#### Acceptance Criteria

1. THE Backend_API SHALL maintain a Session for each connected user that preserves the Agent's conversation history across multiple requests
2. WHEN a user sends a message with a session identifier in the request payload, THE Backend_API SHALL route the message to the existing Session associated with that identifier
3. WHEN a user sends a message without a session identifier, THE Backend_API SHALL create a new Session, assign it a unique session identifier, and return the identifier in the response payload
4. WHEN a request includes a session identifier, THE Backend_API SHALL use the existing Session associated with that identifier and include the same session identifier in the response
5. IF a request includes an invalid or expired session identifier, THEN THE Backend_API SHALL create a new Session, return the new session identifier in the response, and include an indication that a new session was started
6. IF a Session has received no requests for 30 minutes, THEN THE Backend_API SHALL consider that Session expired and eligible for removal

### Requirement 3: Chat Interface Layout

**User Story:** As a user, I want a clean chat interface in my browser, so that I can easily read and send messages to the travel agent.

#### Acceptance Criteria

1. THE Frontend SHALL display a Chat_Window that shows the conversation history between the user and the agent
2. THE Frontend SHALL display a Message_Input at the bottom of the page with a text field that accepts up to 500 characters and a send button
3. THE Frontend SHALL display user messages aligned to the right side of the Chat_Window
4. THE Frontend SHALL display agent messages aligned to the left side of the Chat_Window
5. THE Frontend SHALL visually distinguish user messages from agent messages using different background colors
6. WHEN a new message is added to the Chat_Window, THE Frontend SHALL automatically scroll the Chat_Window to the most recent message
7. THE Frontend SHALL display a timestamp alongside each Chat_Message indicating when the message was sent or received

### Requirement 4: Message Sending

**User Story:** As a user, I want to type a message and send it to the agent, so that I can ask travel questions and receive recommendations.

#### Acceptance Criteria

1. WHEN the user clicks the send button or presses the Enter key (without Shift held), THE Frontend SHALL send the message text (maximum 2000 characters) to the Backend_API
2. WHEN a message is sent, THE Frontend SHALL display the user's message in the Chat_Window before receiving the Backend_API response
3. WHEN a message is sent, THE Frontend SHALL clear the Message_Input text field
4. WHILE the Backend_API is processing a request, THE Frontend SHALL display a Loading_Indicator in the Chat_Window
5. WHEN the Backend_API returns a response, THE Frontend SHALL display the agent's response in the Chat_Window and remove the Loading_Indicator
6. WHILE the Backend_API is processing a request, THE Frontend SHALL disable the send button and Message_Input to prevent duplicate submissions
7. IF the Message_Input is empty or contains only whitespace characters, THEN THE Frontend SHALL disable the send button
8. IF the message text exceeds 2000 characters, THEN THE Frontend SHALL prevent submission and display a character limit indicator

### Requirement 5: Error Handling

**User Story:** As a user, I want to see clear error messages when something goes wrong, so that I know the system encountered a problem and I can try again.

#### Acceptance Criteria

1. IF the Backend_API returns an error response, THEN THE Frontend SHALL display an error message in the Chat_Window indicating the request failed, visually distinct from agent messages through a different background color
2. IF the Frontend cannot reach the Backend_API (network error), THEN THE Frontend SHALL display a connection error message in the Chat_Window, visually distinct from agent messages through a different background color
3. WHEN an error occurs due to an API error response, a network error, or a timeout, THE Frontend SHALL remove the Loading_Indicator, re-enable the Message_Input and send button, and preserve the user's most recent message in the Chat_Window so the user can retry
4. IF the Backend_API request exceeds a 30-second timeout, THEN THE Frontend SHALL abort the request and display a timeout error message in the Chat_Window, visually distinct from agent messages through a different background color

### Requirement 6: Responsive Design

**User Story:** As a user, I want the chat interface to work on different screen sizes, so that I can use it on both desktop and mobile devices.

#### Acceptance Criteria

1. WHILE the viewport width is less than 768 pixels, THE Frontend SHALL render the Chat_Window and Message_Input at 100% of the viewport width
2. WHILE the viewport width is 768 pixels or greater, THE Frontend SHALL center the chat layout horizontally with a maximum width of 800 pixels
3. THE Frontend SHALL use a font size of at least 16 pixels for message text on all screen sizes
4. WHILE the viewport width is less than 768 pixels, THE Frontend SHALL render the send button and Message_Input with a minimum tap target size of 44 by 44 pixels

### Requirement 7: Welcome Experience

**User Story:** As a new user, I want to see a welcome message when I first open the chat, so that I understand what the agent can help me with.

#### Acceptance Criteria

1. WHEN the Frontend loads with no existing session identifier stored, THE Frontend SHALL display a welcome message from the agent in the Chat_Window before any user interaction
2. THE welcome message SHALL mention that the agent can help with destinations, hotels, restaurants, activities, and trip planning in Egypt
3. THE Frontend SHALL display the welcome message as an agent message in the Chat_Window, styled identically to other agent messages (left-aligned with agent background color)
4. WHEN the user sends their first message, THE Frontend SHALL retain the welcome message in the Chat_Window as part of the conversation history
5. IF the Frontend loads with an existing session identifier stored, THEN THE Frontend SHALL NOT display the welcome message
