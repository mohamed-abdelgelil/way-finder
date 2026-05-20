# Egypt Travel Agent — Presentation

---

## Slide 1: System Capabilities

### What It Does

An **AI-powered conversational travel assistant** for Egypt that helps users plan trips through natural language.

### Key Capabilities

| Capability | Description |
|---|---|
| 🏛️ Destination Discovery | Browse and explore 5 Egyptian destinations (Cairo, Luxor, Aswan, Alexandria, Hurghada) |
| 🏨 Hotel Search | Find accommodations filtered by budget — from budget inns to luxury resorts |
| 🍽️ Restaurant Recommendations | Discover dining options by cuisine type and price range |
| 🎯 Activity Finder | Explore tours, cultural visits, and adventures at each destination |
| 📋 Smart Trip Planning | Generate complete trip plans (hotel + dining + activity) within a total budget, with fallback to partial plans |
| 💬 Session Memory | Remembers user preferences across the conversation — no need to repeat yourself |

### User Experience

- Natural language interaction — ask questions like "Plan a trip to Aswan for $200"
- Budget-aware — suggests alternatives when budget is too low
- Available via Jupyter Notebook (interactive) or Web UI (FastAPI backend)

---

## Slide 2: Technology & Architecture

### Tech Stack

| Layer | Technology |
|---|---|
| AI Framework | **Strands Agents SDK** (Python) |
| LLM Provider | **Amazon Bedrock** |
| Model | **Amazon Nova 2 Lite** / **Claude Sonnet** |
| Web Backend | **FastAPI** with async support |
| Entry Points | Jupyter Notebook + REST API |
| Language | Python 3.11+ |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                         │
│         (Jupyter Notebook / Web UI + FastAPI)             │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Strands Agent (Orchestrator)                 │
│         System Prompt + Session Memory (30 min TTL)      │
└──────────────────────────┬──────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
┌──────────────────┐ ┌──────────┐ ┌──────────────────┐
│  Amazon Bedrock  │ │  Tools   │ │  Session Manager │
│  (LLM Calls)    │ │  Layer   │ │  (In-Memory)     │
└──────────────────┘ └────┬─────┘ └──────────────────┘
                          │
          ┌───────┬───────┼───────┬───────┐
          ▼       ▼       ▼       ▼       ▼
      Destinations  Hotels  Restaurants  Activities  Trip Planner
          │       │       │       │       │
          └───────┴───────┴───────┴───────┘
                          │
                          ▼
              ┌──────────────────────┐
              │   travel_data.py     │
              │ (Single Source of    │
              │      Truth)          │
              └──────────────────────┘
```

### Design Principles

- **Tool-based architecture** — each domain (hotels, restaurants, etc.) is a self-contained `@tool` module
- **Single data source** — all travel data lives in `travel_data.py`, tools are read-only
- **Graceful degradation** — budget too low? Get partial plans instead of errors
- **Stateless tools, stateful agent** — tools are pure functions; the agent manages conversation context

---
