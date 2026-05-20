# Design Document

## Overview

This document describes the architecture and design of the Egypt Travel Agent, an AI-powered conversational assistant built with the Strands Agents SDK on Amazon Bedrock. The agent provides Egypt travel recommendations through modular `@tool`-decorated Python functions, session-based conversation memory, and budget-aware filtering logic. The system is delivered as a single Jupyter notebook with supporting tool modules.

## Architecture

The system follows a tool-augmented agent architecture where the Strands Agent orchestrates calls to specialized tool functions based on user queries. The architecture consists of three layers:

1. **Agent Layer** — Strands Agent configured with Amazon Bedrock (Claude Sonnet), responsible for natural language understanding, tool selection, and response generation
2. **Tool Layer** — Python modules with `@tool`-decorated functions providing structured access to travel data with filtering capabilities
3. **Data Layer** — Hardcoded Python dictionaries containing Egypt travel information

```
┌─────────────────────────────────────────────────┐
│              Jupyter Notebook                     │
│  ┌───────────────────────────────────────────┐  │
│  │         Interactive Demo Section           │  │
│  └───────────────────┬───────────────────────┘  │
│                      │                           │
│  ┌───────────────────▼───────────────────────┐  │
│  │          Strands Agent                     │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │  Amazon Bedrock (Claude Sonnet)     │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │  Session Memory                     │  │  │
│  │  │  (manage_conversation_history)      │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  └───────┬────────┬────────┬────────┬────────┘  │
│          │        │        │        │            │
│  ┌───────▼──┐ ┌───▼───┐ ┌──▼────┐ ┌─▼───────┐  │
│  │Destination│ │ Hotel │ │Restau-│ │Activity │  │
│  │  Tool    │ │ Tool  │ │rant   │ │  Tool   │  │
│  │          │ │       │ │ Tool  │ │         │  │
│  └───────┬──┘ └───┬───┘ └──┬────┘ └─┬───────┘  │
│          │        │        │        │            │
│  ┌───────▼────────▼────────▼────────▼────────┐  │
│  │           Travel Data (Python Dicts)       │  │
│  │  destinations | hotels | restaurants |     │  │
│  │  activities                                │  │
│  └────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Travel Data Module (`travel_data.py`)

Stores all Egypt travel information as Python dictionaries. Serves as the single source of truth for all tool functions.

```python
# travel_data.py

DESTINATIONS = {
    "cairo": {
        "name": "Cairo",
        "description": "Egypt's sprawling capital, home to the Pyramids of Giza and the Egyptian Museum.",
        "region": "Lower Egypt"
    },
    "luxor": {
        "name": "Luxor",
        "description": "Ancient Thebes, featuring the Valley of the Kings and Karnak Temple.",
        "region": "Upper Egypt"
    },
    # ... at least 5 destinations total
}

HOTELS = {
    "cairo": [
        {"name": "Marriott Mena House", "price_per_night": 250, "rating": 4.8},
        {"name": "Cairo Budget Inn", "price_per_night": 45, "rating": 3.5},
        # ... at least 2 per destination
    ],
    # ...
}

RESTAURANTS = {
    "cairo": [
        {"name": "Abou El Sid", "cuisine_type": "Egyptian", "price_range": 30},
        {"name": "Sequoia", "cuisine_type": "Mediterranean", "price_range": 55},
        # ... at least 2 per destination
    ],
    # ...
}

ACTIVITIES = {
    "cairo": [
        {"name": "Pyramids of Giza Tour", "description": "Guided tour of the Great Pyramids and Sphinx", "cost": 60},
        {"name": "Egyptian Museum Visit", "description": "Explore ancient artifacts and mummies", "cost": 25},
        # ... at least 2 per destination
    ],
    # ...
}
```

### 2. Destination Tool Module (`destination_tool.py`)

```python
from strands import tool
from travel_data import DESTINATIONS

@tool
def get_destinations() -> str:
    """Get all available Egypt travel destinations."""
    # Returns formatted list of all destination names and descriptions
    ...

@tool
def get_destination_details(destination: str) -> str:
    """Get detailed information about a specific Egypt destination.
    
    Args:
        destination: Name of the destination (case-insensitive)
    """
    # Returns destination details including description, region,
    # and summary of available hotels, restaurants, activities
    ...
```

### 3. Hotel Tool Module (`hotel_tool.py`)

```python
from strands import tool
from travel_data import HOTELS

@tool
def get_hotels(destination: str, budget: float = None) -> str:
    """Get hotel recommendations for a destination, optionally filtered by budget.
    
    Args:
        destination: Name of the destination (case-insensitive)
        budget: Maximum price per night in USD (optional)
    """
    # Returns hotels for destination
    # If budget provided, filters to price_per_night <= budget
    # If no matches with budget, suggests nearest available options
    ...
```

### 4. Restaurant Tool Module (`restaurant_tool.py`)

```python
from strands import tool
from travel_data import RESTAURANTS

@tool
def get_restaurants(destination: str, cuisine: str = None, budget: float = None) -> str:
    """Get restaurant recommendations for a destination.
    
    Args:
        destination: Name of the destination (case-insensitive)
        cuisine: Preferred cuisine type (optional)
        budget: Maximum price per meal in USD (optional)
    """
    # Returns restaurants for destination
    # If cuisine provided, filters by cuisine_type match
    # If budget provided, filters to price_range <= budget
    ...
```

### 5. Activity Tool Module (`activity_tool.py`)

```python
from strands import tool
from travel_data import ACTIVITIES

@tool
def get_activities(destination: str, budget: float = None) -> str:
    """Get activity recommendations for a destination, optionally filtered by budget.
    
    Args:
        destination: Name of the destination (case-insensitive)
        budget: Maximum activity cost in USD (optional)
    """
    # Returns activities for destination
    # If budget provided, filters to cost <= budget
    # If no matches with budget, suggests nearest available options
    ...
```

### 6. Trip Planner Tool Module (`trip_planner_tool.py`)

```python
from strands import tool
from travel_data import HOTELS, RESTAURANTS, ACTIVITIES

@tool
def plan_trip(destination: str, total_budget: float, nights: int = 1) -> str:
    """Plan a complete trip within a total budget.
    
    Args:
        destination: Name of the destination (case-insensitive)
        total_budget: Total trip budget in USD
        nights: Number of nights for accommodation (default 1)
    """
    # Finds combinations of hotel (price * nights) + restaurant + activity
    # that fit within total_budget
    # Returns cost breakdown by category
    # If no complete plan fits, returns minimum budget and partial plans
    ...
```

### 7. Agent Configuration (in Notebook)

```python
from strands import Agent
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514",
    region_name="us-east-1"
)

agent = Agent(
    model=model,
    tools=[get_destinations, get_destination_details, get_hotels, 
           get_restaurants, get_activities, plan_trip],
    system_prompt=EGYPT_TRAVEL_SYSTEM_PROMPT,
    conversation_manager=None  # Uses default sliding window
)
```

### 8. Session Memory Management

The agent uses the Strands `manage_conversation_history` pattern for session-based memory. This maintains conversation context within a single session, allowing the agent to reference previously stated preferences (destination, budget) without the user repeating them.

```python
# Conversation loop with session memory
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        break
    response = agent(user_input)
    print(f"Agent: {response}")
```

The agent's conversation history is maintained automatically by the Strands SDK within the `Agent` instance. Each call to `agent(user_input)` appends to the existing conversation history, preserving context.

## Interfaces

### Tool Function Signatures

| Tool | Input Parameters | Return Type |
|------|-----------------|-------------|
| `get_destinations()` | None | `str` (formatted destination list) |
| `get_destination_details(destination)` | `destination: str` | `str` (destination details) |
| `get_hotels(destination, budget)` | `destination: str, budget: float = None` | `str` (hotel list) |
| `get_restaurants(destination, cuisine, budget)` | `destination: str, cuisine: str = None, budget: float = None` | `str` (restaurant list) |
| `get_activities(destination, budget)` | `destination: str, budget: float = None` | `str` (activity list) |
| `plan_trip(destination, total_budget, nights)` | `destination: str, total_budget: float, nights: int = 1` | `str` (trip plan) |

### Data Access Patterns

All tools access the Travel_Data dictionaries using case-insensitive destination name lookup:

```python
def _normalize_destination(destination: str) -> str:
    """Normalize destination name for dictionary lookup."""
    return destination.strip().lower()

def _get_items_for_destination(data_dict: dict, destination: str) -> list:
    """Retrieve items for a normalized destination key."""
    key = _normalize_destination(destination)
    return data_dict.get(key, [])
```

## Data Models

### Destination

```python
{
    "name": str,           # Display name (e.g., "Cairo")
    "description": str,    # Brief description of the destination
    "region": str          # Geographic region within Egypt
}
```

### Hotel

```python
{
    "name": str,           # Hotel name
    "price_per_night": float,  # Cost per night in USD (numeric)
    "rating": float        # Rating out of 5.0
}
```

### Restaurant

```python
{
    "name": str,           # Restaurant name
    "cuisine_type": str,   # Type of cuisine (e.g., "Egyptian", "Mediterranean")
    "price_range": float   # Average meal cost in USD (numeric)
}
```

### Activity

```python
{
    "name": str,           # Activity name
    "description": str,    # Brief description of the activity
    "cost": float          # Cost per person in USD (numeric)
}
```

### Trip Plan (Output)

```python
{
    "destination": str,
    "nights": int,
    "accommodation": {"name": str, "cost": float},  # price_per_night * nights
    "dining": {"name": str, "cost": float},
    "activity": {"name": str, "cost": float},
    "total_cost": float,
    "budget_remaining": float
}
```

## Error Handling

| Scenario | Handling Strategy |
|----------|------------------|
| Invalid destination name | Return message listing available destinations |
| Budget below minimum available option | Return empty results with nearest available price suggestion |
| No restaurants matching cuisine type | Return message indicating no match, list available cuisine types |
| Budget of 0 or negative value | Treat as no budget filter (return all items) or return validation error |
| Empty Travel_Data for a category | Return message indicating no data available for that category |
| Non-numeric budget input | Tool parameter validation rejects; agent asks user to provide a number |

## Notebook Structure

The Jupyter notebook follows this sequential structure:

1. **Setup Section** — Install dependencies (`strands-agents`, `strands-agents-tools`), configure AWS credentials, import modules
2. **Travel Data Section** — Define or import the Travel_Data dictionaries
3. **Tool Definitions Section** — Define or import all `@tool`-decorated functions
4. **Agent Creation Section** — Configure and instantiate the Strands Agent with Bedrock model and tools
5. **Interactive Demo Section** — Conversation loop with example queries covering all capabilities

## Testing Strategy

### Unit Tests
- Verify each tool returns correct data for specific known destinations
- Verify output format contains required fields (name, price, rating, etc.)
- Verify edge cases: invalid destination names, zero/negative budgets, no matching results

### Property Tests
- Budget filtering invariants across all tools (Properties 3, 5)
- Data retrieval completeness (Properties 1, 2)
- Cost calculation correctness (Property 6)
- Data type invariants (Property 7)
- Cuisine filtering correctness (Property 4)

### Integration Tests
- Session memory persistence across multi-turn conversations
- Agent tool selection for different query types
- End-to-end conversation flow with Bedrock model

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Destination data retrieval completeness

For any Travel_Data dictionary containing N destinations, the `get_destinations` tool shall return exactly N destination entries, and for any valid destination key, `get_destination_details` shall return data matching the stored dictionary entry for that key.

**Validates: Requirements 1.1, 1.2, 1.3**

### Property 2: Category data retrieval by destination

For any valid destination and any category (hotels, restaurants, activities), the corresponding tool shall return all items associated with that destination in Travel_Data, with no items omitted and no items from other destinations included.

**Validates: Requirements 2.1, 3.1, 4.1**

### Property 3: Budget filtering correctness

For any numeric budget value and any destination, every item returned by a budget-filtered tool query shall have its price field (price_per_night for hotels, price_range for restaurants, cost for activities) less than or equal to the specified budget amount.

**Validates: Requirements 2.2, 3.3, 4.2**

### Property 4: Cuisine filtering correctness

For any cuisine type filter string and any destination, every restaurant returned by the filtered query shall have a cuisine_type field matching the specified filter (case-insensitive comparison).

**Validates: Requirements 3.2**

### Property 5: Trip plan budget constraint

For any total budget amount and destination, every trip plan combination returned by the plan_trip tool shall have a total_cost (accommodation + dining + activity) less than or equal to the specified total budget.

**Validates: Requirements 5.1**

### Property 6: Trip cost calculation correctness

For any trip plan returned by the plan_trip tool, the reported total_cost shall equal the sum of the individual category costs (hotel price_per_night × nights + restaurant price_range + activity cost).

**Validates: Requirements 5.2**

### Property 7: Price data type invariant

For any entry in Travel_Data across all categories (hotels, restaurants, activities), all price-related fields (price_per_night, price_range, cost) shall be numeric values (int or float) representing US dollar amounts.

**Validates: Requirements 8.5**
