# app.py
# FastAPI backend for the Egypt Travel Agent web interface

import asyncio
import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from session_manager import SessionStore

logger = logging.getLogger(__name__)

app = FastAPI(title="Egypt Travel Agent API")

# CORS middleware — allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global session store
session_store = SessionStore()

# Ensure static directory exists
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)


# --- Pydantic Models ---

class ChatRequest(BaseModel):
    message: str | None = None
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    new_session: bool = False


class ErrorResponse(BaseModel):
    error: str


# --- Endpoints ---

@app.post("/chat")
async def chat(request: Request) -> JSONResponse:
    """Process a chat message and return the agent's response."""
    # Parse JSON body
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid request format"},
        )

    # Validate message field
    message = body.get("message") if isinstance(body, dict) else None

    if message is None or not isinstance(message, str):
        return JSONResponse(
            status_code=400,
            content={"error": "Message field is required and must be non-empty"},
        )

    if len(message.strip()) == 0:
        return JSONResponse(
            status_code=400,
            content={"error": "Message field is required and must be non-empty"},
        )

    if len(message) > 2000:
        return JSONResponse(
            status_code=400,
            content={"error": "Message must not exceed 2000 characters"},
        )

    # Session lookup or creation
    session_id = body.get("session_id") if isinstance(body, dict) else None
    new_session = False

    agent = None
    if session_id:
        agent = session_store.get_session(session_id)

    if agent is None:
        session_id = session_store.create_session()
        agent = session_store.get_session(session_id)
        new_session = True

    # Call the agent with timeout
    try:
        result = await asyncio.wait_for(
            asyncio.to_thread(agent, message),
            timeout=60.0,
        )
        response_text = str(result)
    except asyncio.TimeoutError:
        return JSONResponse(
            status_code=504,
            content={"error": "Request timed out. Please try a simpler question."},
        )
    except Exception:
        logger.exception("Agent error during message processing")
        return JSONResponse(
            status_code=500,
            content={"error": "The travel agent encountered an error. Please try again."},
        )

    return JSONResponse(
        status_code=200,
        content={
            "response": response_text,
            "session_id": session_id,
            "new_session": new_session,
        },
    )


# --- Static file serving ---

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    """Serve the frontend HTML page."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(
        status_code=404,
        content={"error": "Frontend not found. Place index.html in the static/ directory."},
    )
