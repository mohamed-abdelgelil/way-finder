# Project Structure

```
way-finder/
├── egypt_travel_agent.ipynb   # Entry point — agent setup and interactive loop
├── travel_data.py             # Single source of truth for all travel data (dicts)
├── destination_tool.py        # @tool: get_destinations, get_destination_details
├── hotel_tool.py              # @tool: get_hotels
├── restaurant_tool.py         # @tool: get_restaurants
├── activity_tool.py           # @tool: get_activities
├── trip_planner_tool.py       # @tool: plan_trip (combines hotel + restaurant + activity)
└── test_integration.py        # unittest integration tests for all tools
```

## Conventions

### One tool per file
Each tool module contains exactly one public `@tool` function (destination_tool.py has two). File name matches the tool's domain.

### Data access pattern
Tool modules import directly from `travel_data.py`. They never mutate the data — all lookups are read-only.

### Destination normalization
Every tool module defines a local `_normalize_destination(destination: str) -> str` helper that lowercases and strips the input before dict lookup. This is duplicated intentionally across modules to keep them self-contained.

### Return type: always `str`
All `@tool` functions return a plain formatted string. The agent reads this string as tool output.

### Error handling
Invalid destination → return a "not found" message listing valid destinations.  
Budget too low → return a "no results" message with nearest alternatives.  
Never raise exceptions from tool functions.

### Adding a new destination
1. Add an entry to each of the four dicts in `travel_data.py`: `DESTINATIONS`, `HOTELS`, `RESTAURANTS`, `ACTIVITIES`
2. No changes needed in tool files — they iterate the dicts dynamically

### Adding a new tool
1. Create a new `*_tool.py` file following the existing pattern
2. Decorate the function with `@tool` and import from `travel_data`
3. Register the function in the `tools=[...]` list in the notebook
