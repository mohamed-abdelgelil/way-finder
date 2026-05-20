# Implementation Plan: Egypt Travel Agent

## Overview

Build an AI-powered Egypt travel assistant using the Strands Agents SDK with Amazon Bedrock. The implementation creates a modular tool-based architecture with hardcoded travel data, budget-aware filtering, and session-based conversation memory, delivered as a Jupyter notebook with supporting Python modules.

## Tasks

- [x] 1. Create travel data module
  - [x] 1.1 Create `travel_data.py` with destination, hotel, restaurant, and activity dictionaries
    - Define DESTINATIONS dict with at least 5 Egypt destinations (Cairo, Luxor, Aswan, Alexandria, Hurghada) each with name, description, and region
    - Define HOTELS dict keyed by destination with at least 2 hotels per destination, each with name, price_per_night (numeric USD), and rating
    - Define RESTAURANTS dict keyed by destination with at least 2 restaurants per destination, each with name, cuisine_type, and price_range (numeric USD)
    - Define ACTIVITIES dict keyed by destination with at least 2 activities per destination, each with name, description, and cost (numeric USD)
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

  - [ ]* 1.2 Write property tests for travel data structure
    - **Property 7: Price data type invariant**
    - Verify all price fields (price_per_night, price_range, cost) are numeric (int or float)
    - Verify minimum data counts per destination (at least 2 items per category)
    - **Validates: Requirements 8.5, 8.2, 8.3, 8.4**

- [x] 2. Implement destination tool
  - [x] 2.1 Create `destination_tool.py` with `get_destinations` and `get_destination_details` functions
    - Implement `get_destinations()` decorated with `@tool` that returns formatted list of all destinations
    - Implement `get_destination_details(destination: str)` decorated with `@tool` that returns details for a specific destination
    - Add `_normalize_destination()` helper for case-insensitive lookup
    - Handle invalid destination names by returning available destinations list
    - _Requirements: 1.1, 1.2, 1.3, 7.1_

  - [ ]* 2.2 Write property test for destination data retrieval
    - **Property 1: Destination data retrieval completeness**
    - For any Travel_Data with N destinations, `get_destinations` returns exactly N entries
    - For any valid key, `get_destination_details` returns matching data
    - **Validates: Requirements 1.1, 1.2, 1.3**

- [x] 3. Implement hotel tool
  - [x] 3.1 Create `hotel_tool.py` with `get_hotels` function
    - Implement `get_hotels(destination: str, budget: float = None)` decorated with `@tool`
    - Return hotel name, price per night, and rating for each result
    - Filter by budget when provided (price_per_night <= budget)
    - When no hotels match budget, suggest nearest available price options
    - Handle invalid destination with error message listing available destinations
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 7.1_

  - [ ]* 3.2 Write property test for hotel budget filtering
    - **Property 3: Budget filtering correctness (hotels)**
    - For any budget and destination, all returned hotels have price_per_night <= budget
    - **Validates: Requirements 2.2**

  - [ ]* 3.3 Write property test for hotel data retrieval by destination
    - **Property 2: Category data retrieval by destination (hotels)**
    - All hotels for a destination are returned with no omissions and no cross-destination contamination
    - **Validates: Requirements 2.1**

- [x] 4. Implement restaurant tool
  - [x] 4.1 Create `restaurant_tool.py` with `get_restaurants` function
    - Implement `get_restaurants(destination: str, cuisine: str = None, budget: float = None)` decorated with `@tool`
    - Return restaurant name, cuisine type, and price range for each result
    - Filter by cuisine type when provided (case-insensitive match)
    - Filter by budget when provided (price_range <= budget)
    - Handle no matches by listing available cuisine types
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 7.1_

  - [ ]* 4.2 Write property test for restaurant budget filtering
    - **Property 3: Budget filtering correctness (restaurants)**
    - For any budget and destination, all returned restaurants have price_range <= budget
    - **Validates: Requirements 3.3**

  - [ ]* 4.3 Write property test for cuisine filtering
    - **Property 4: Cuisine filtering correctness**
    - For any cuisine filter, all returned restaurants have matching cuisine_type (case-insensitive)
    - **Validates: Requirements 3.2**

- [x] 5. Implement activity tool
  - [x] 5.1 Create `activity_tool.py` with `get_activities` function
    - Implement `get_activities(destination: str, budget: float = None)` decorated with `@tool`
    - Return activity name, description, and cost for each result
    - Filter by budget when provided (cost <= budget)
    - When no activities match budget, suggest nearest available cost options
    - Handle invalid destination with error message
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 7.1_

  - [ ]* 5.2 Write property test for activity budget filtering
    - **Property 3: Budget filtering correctness (activities)**
    - For any budget and destination, all returned activities have cost <= budget
    - **Validates: Requirements 4.2**

- [x] 6. Checkpoint - Verify all tools work independently
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Implement trip planner tool
  - [x] 7.1 Create `trip_planner_tool.py` with `plan_trip` function
    - Implement `plan_trip(destination: str, total_budget: float, nights: int = 1)` decorated with `@tool`
    - Find combinations of hotel (price_per_night × nights) + restaurant + activity within total_budget
    - Return cost breakdown by category (accommodation, dining, activities) and total cost
    - If no complete plan fits, return minimum budget required and suggest partial plans
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 7.1_

  - [ ]* 7.2 Write property test for trip plan budget constraint
    - **Property 5: Trip plan budget constraint**
    - For any total budget and destination, every returned plan has total_cost <= total_budget
    - **Validates: Requirements 5.1**

  - [ ]* 7.3 Write property test for trip cost calculation
    - **Property 6: Trip cost calculation correctness**
    - For any trip plan, total_cost == hotel price_per_night × nights + restaurant price_range + activity cost
    - **Validates: Requirements 5.2**

- [x] 8. Create Jupyter notebook with agent configuration
  - [x] 8.1 Create the notebook with setup section
    - Add cells for installing dependencies (`strands-agents`, `strands-agents-tools`)
    - Add AWS credentials configuration guidance
    - Import all tool modules
    - _Requirements: 7.4, 9.1_

  - [x] 8.2 Add agent creation section to notebook
    - Configure BedrockModel with `us.anthropic.claude-sonnet-4-20250514` and `us-east-1` region
    - Create Agent instance with all tools, system prompt, and default conversation manager
    - Define EGYPT_TRAVEL_SYSTEM_PROMPT with Egypt travel specialization instructions
    - _Requirements: 7.3, 6.4_

  - [x] 8.3 Add interactive demo section to notebook
    - Implement conversation loop with session memory (input/response cycle)
    - Add example queries demonstrating: destination discovery, hotel search with budget, restaurant search with cuisine filter, activity search, and budget-based trip planning
    - Ensure agent responds in natural conversational language
    - _Requirements: 6.1, 6.2, 6.3, 9.1, 9.2, 9.3_

- [x] 9. Checkpoint - Ensure tool modules are importable and notebook structure is complete
  - Ensure all tests pass, ask the user if questions arise.

- [x] 10. Wire all components together and verify integration
  - [x] 10.1 Ensure all tool modules are importable from the notebook
    - Verify import paths work correctly between notebook and tool modules
    - Verify agent can call each tool and receive formatted responses
    - Test session memory persists user preferences across multiple agent calls
    - _Requirements: 7.2, 6.1, 6.2, 6.3_

  - [ ]* 10.2 Write integration tests for multi-turn conversation flows
    - Test that destination preference carries across turns
    - Test that budget preference applies to subsequent queries
    - Test tool selection for different query types
    - _Requirements: 6.1, 6.2, 6.3_

- [x] 11. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- The implementation language is Python throughout
- All tool modules use the Strands `@tool` decorator pattern
- Budget filtering uses simple numeric comparison (<=) across all tools

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "2.1"] },
    { "id": 2, "tasks": ["2.2", "3.1", "4.1", "5.1"] },
    { "id": 3, "tasks": ["3.2", "3.3", "4.2", "4.3", "5.2"] },
    { "id": 4, "tasks": ["7.1"] },
    { "id": 5, "tasks": ["7.2", "7.3", "8.1"] },
    { "id": 6, "tasks": ["8.2"] },
    { "id": 7, "tasks": ["8.3"] },
    { "id": 8, "tasks": ["10.1"] },
    { "id": 9, "tasks": ["10.2"] }
  ]
}
```
