# Requirements Document

## Introduction

The Web Search Layer extends the Egypt Travel Agent with real-time web search capabilities. After the agent provides recommendations from its hardcoded travel data, it searches the web for actual booking options on travel platforms (Trivago, Booking.com, Expedia, TripAdvisor, etc.) that match the user's criteria. The results complement the local recommendations by providing clickable links to real booking pages, giving users a path from recommendation to reservation.

## Glossary

- **Agent**: The Strands Agents SDK-based conversational AI assistant that processes user queries and returns travel recommendations for Egypt
- **Web_Search_Tool**: A new `@tool`-decorated Python function that performs web searches targeting travel booking platforms and returns structured results with booking links
- **Search_Query**: A constructed search string combining the user's criteria (destination, budget, dates, preferences) with travel platform site targeting
- **Booking_Platform**: An online travel booking website such as Trivago, Booking.com, Expedia, or TripAdvisor where users can reserve hotels, restaurants, or activities
- **Local_Results**: Recommendations returned from the hardcoded Travel_Data dictionaries (the existing behavior)
- **Web_Results**: Search results retrieved from the web containing real booking options with URLs, titles, prices, and platform names
- **Search_Provider**: The underlying HTTP-based search service used to execute web queries (e.g., a search API or web scraping mechanism)
- **Travel_Data**: Hardcoded Python dictionaries containing all Egypt travel information including destinations, hotels, restaurants, and activities with associated prices

## Requirements

### Requirement 1: Web Search Tool Definition

**User Story:** As a developer, I want a new web search tool module following the existing project conventions, so that the agent can search the web for real booking options.

#### Acceptance Criteria

1. THE Web_Search_Tool SHALL be implemented as a `@tool`-decorated Python function in a dedicated `web_search_tool.py` module
2. THE Web_Search_Tool SHALL accept parameters for destination (str, required), category (str, one of "hotels", "restaurants", "activities"), budget (float, optional), and preferences (str, optional)
3. THE Web_Search_Tool SHALL return a formatted string containing web search results, consistent with the return type convention of existing tools
4. IF the Search_Provider is unavailable or returns an error, THEN THE Web_Search_Tool SHALL return a descriptive error message without raising an exception
5. THE Web_Search_Tool SHALL include a `_normalize_destination()` helper for case-insensitive destination lookup, consistent with existing tool modules

### Requirement 2: Travel Platform Targeting

**User Story:** As a traveler, I want the web search to focus on reputable travel booking sites, so that I get relevant and trustworthy booking options.

#### Acceptance Criteria

1. WHEN constructing a Search_Query, THE Web_Search_Tool SHALL include site-restriction operators (e.g., "site:trivago.com OR site:booking.com OR site:expedia.com OR site:tripadvisor.com") to limit results to the defined Booking_Platforms
2. THE Web_Search_Tool SHALL construct each Search_Query by concatenating the destination name, the category (hotels, restaurants, or activities), and all user-provided non-empty filter values (budget, dates, preferences) separated by spaces
3. WHEN a user specifies a budget, THE Web_Search_Tool SHALL include the budget amount with a currency indicator (e.g., "under $150") in the Search_Query
4. THE Web_Search_Tool SHALL append "Egypt" to every Search_Query that contains a destination name
5. IF the user provides no destination, no category, and no filters, THEN THE Web_Search_Tool SHALL return a message indicating that at least a destination or category is required to perform a search

### Requirement 3: Search Result Formatting

**User Story:** As a traveler, I want web search results presented with clickable links and key details, so that I can easily navigate to booking pages.

#### Acceptance Criteria

1. THE Web_Search_Tool SHALL return each Web_Result with a title, URL, source platform name, and a description snippet of no more than 150 characters
2. WHEN presenting Web_Results, THE Web_Search_Tool SHALL format each result as a markdown link in the form `[title](URL)` followed by the source platform name and description snippet on subsequent lines
3. THE Web_Search_Tool SHALL return a maximum of 5 Web_Results per search to keep responses concise
4. IF no Web_Results are found for a query, THEN THE Web_Search_Tool SHALL return a message indicating no online booking options were found and suggest removing optional filters such as budget or date constraints
5. IF a Web_Result is missing a title or description snippet, THEN THE Web_Search_Tool SHALL omit that result from the formatted output and proceed with the remaining results

### Requirement 4: Complementary Presentation

**User Story:** As a traveler, I want web booking options shown alongside the local recommendations, so that I can compare curated suggestions with real online availability.

#### Acceptance Criteria

1. WHEN the Agent provides Local_Results for a travel query, THE Agent SHALL invoke the Web_Search_Tool using the same destination, category, and budget parameters that were used to retrieve the Local_Results
2. THE Agent SHALL present Web_Results after the Local_Results, with a section heading labeled "Online Booking Options" to separate them from the local recommendations
3. THE Agent SHALL label Local_Results as "Curated Recommendations" and Web_Results as "Online Booking Links" so that the user can identify the source of each set of results
4. WHEN the Agent presents Web_Results, THE Agent SHALL include a disclaimer note stating that prices and availability on external platforms may differ from the local recommendations
5. IF the Web_Search_Tool returns an error or no results, THEN THE Agent SHALL still present the Local_Results and display a message indicating that online booking options could not be retrieved at this time

### Requirement 5: Criteria Matching

**User Story:** As a traveler, I want the web search to use my stated preferences, so that the online results are relevant to what I am looking for.

#### Acceptance Criteria

1. WHEN a user has specified a destination, THE Web_Search_Tool SHALL include that destination name in the Search_Query
2. WHEN a user has specified a budget, THE Web_Search_Tool SHALL include budget constraints in the Search_Query to find options within 20% above the stated price range
3. WHEN a user has specified dates or number of nights, THE Web_Search_Tool SHALL include the specified dates or duration in the Search_Query as check-in/check-out dates or number of nights
4. WHEN a user has specified preferences (cuisine type, activity type, hotel rating), THE Web_Search_Tool SHALL include each stated preference as a distinct term in the Search_Query
5. WHEN a user has specified multiple criteria (destination, budget, dates, preferences), THE Web_Search_Tool SHALL combine all specified criteria into a single Search_Query
6. IF the user has not specified any criteria beyond a general travel interest, THEN THE Web_Search_Tool SHALL construct the Search_Query using only the destination and category without additional filter terms

### Requirement 6: Agent Integration

**User Story:** As a developer, I want the web search tool registered with the agent, so that the agent can invoke it alongside existing tools.

#### Acceptance Criteria

1. THE Web_Search_Tool SHALL be imported from `web_search_tool.py` and added to the Agent's tools list in the Notebook, preserving all existing tools (get_destinations, get_destination_details, get_hotels, get_restaurants, get_activities, plan_trip)
2. THE Agent system prompt SHALL be updated to instruct the Agent to invoke the Web_Search_Tool for matching online booking options after presenting Local_Results for hotel, restaurant, or activity queries
3. WHEN a user explicitly asks for online booking links without a preceding local query, THE Agent SHALL invoke the Web_Search_Tool independently using the user's stated criteria
4. WHILE the Web_Search_Tool is registered, THE Agent SHALL produce identical Local_Results from existing tools (get_hotels, get_restaurants, get_activities, plan_trip) as when the Web_Search_Tool is not registered
5. IF the Web_Search_Tool returns an error message, THEN THE Agent SHALL still present the Local_Results to the user and append a note indicating that online booking options are temporarily unavailable

### Requirement 7: Search Provider Configuration

**User Story:** As a developer, I want the search provider to be configurable, so that the implementation can use different search backends without changing the tool interface.

#### Acceptance Criteria

1. THE Web_Search_Tool SHALL use a standard HTTP library (requests or httpx) to execute web searches against the configured Search_Provider endpoint
2. THE Web_Search_Tool SHALL read the search API endpoint URL from the environment variable `SEARCH_API_URL` and the API key from `SEARCH_API_KEY`
3. IF the `SEARCH_API_KEY` environment variable is not set, THEN THE Web_Search_Tool SHALL return a message stating "Web search is not configured. Set SEARCH_API_KEY to enable online booking search."
4. THE Web_Search_Tool SHALL handle rate limiting (HTTP 429) or quota errors from the Search_Provider by returning a message stating "Web search is temporarily unavailable due to rate limiting. Please try again later."
5. IF the Search_Provider returns an HTTP error status (4xx or 5xx other than 429), THEN THE Web_Search_Tool SHALL return a generic error message without exposing the raw HTTP response details
