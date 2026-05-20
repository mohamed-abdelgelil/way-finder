"""
FastAPI backend for the Egypt Travel Agent chatbot.
Uses an intent-based router to call travel tools directly.
(Swap intent_router for agent_session when a capable LLM is available.)
"""

import sys
import os

# Ensure the project root (where tool modules live) is on the path
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Ensure the backend directory is on the path for sibling imports
_backend_dir = os.path.dirname(os.path.abspath(__file__))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from intent_router import process_message, clear_session

app = FastAPI(title="Egypt Travel Agent API", version="1.0.0")

# Allow the React dev server and any localhost origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        response_text = process_message(req.session_id, req.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    return ChatResponse(session_id=req.session_id, response=response_text)


@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    clear_session(session_id)
    return {"status": "cleared", "session_id": session_id}
