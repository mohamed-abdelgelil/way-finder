# Product: Egypt Travel Agent

An AI-powered conversational travel assistant for Egypt. Users interact with a Strands Agent (backed by Amazon Bedrock / Claude Sonnet) that calls a set of Python tools to look up destinations, hotels, restaurants, and activities, and to plan complete trips within a budget.

## Scope

- Covers 5 Egyptian destinations: Cairo, Luxor, Aswan, Alexandria, Hurghada
- All travel data (destinations, hotels, restaurants, activities) lives in a single source-of-truth file: `travel_data.py`
- The agent maintains session memory across a conversation — users state preferences once and the agent reuses them

## Key Capabilities

- Discover and describe destinations
- Filter hotels, restaurants, and activities by budget
- Generate complete trip plans (accommodation + dining + activity) within a total budget, with fallback to partial plans when the budget is too low
