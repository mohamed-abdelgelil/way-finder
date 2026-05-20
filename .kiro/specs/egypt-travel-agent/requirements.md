# Requirements Document

## Introduction

The Egypt Travel Agent is an AI-powered conversational assistant specialized in Egypt tourism. Built using the Strands Agents SDK with Amazon Bedrock (Claude Sonnet), the agent helps users discover destinations, select hotels, find restaurants, and plan activities across Egypt based on their preferences and budget. The system is delivered as a single Jupyter notebook with supporting Python tool modules, using hardcoded travel data dictionaries and session-based conversation memory.

## Glossary

- **Agent**: The Strands Agents SDK-based conversational AI assistant that processes user queries and returns travel recommendations for Egypt
- **Tool**: A Python function decorated with `@tool` that provides the Agent with access to specific travel data or functionality
- **Destination**: A geographic location in Egypt available for tourist visits, stored as a dictionary entry with metadata
- **Hotel**: An accommodation option associated with a Destination, including name, price per night, and rating
- **Restaurant**: A dining establishment associated with a Destination, including name, cuisine type, and price range
- **Activity**: A tourist activity or experience available at a Destination, including name, description, and cost
- **Budget**: A numeric dollar amount provided by the user representing their maximum spending threshold for filtering recommendations
- **Session_Memory**: The Strands session management mechanism that maintains conversation context within a single user session using the manage_conversation_history pattern
- **Notebook**: The single Jupyter notebook file containing setup instructions, tool definitions, agent creation, and interactive demo sections
- **Travel_Data**: Hardcoded Python dictionaries containing all Egypt travel information including destinations, hotels, restaurants, and activities with associated prices

## Requirements

### Requirement 1: Destination Discovery

**User Story:** As a traveler, I want to explore available destinations in Egypt, so that I can decide where to visit.

#### Acceptance Criteria

1. WHEN a user asks about available destinations, THE Agent SHALL return a list of all Egypt destinations from the Travel_Data
2. WHEN a user asks about a specific destination, THE Agent SHALL return detailed information about that destination including description and available options
3. THE Destination Tool SHALL provide access to destination names, descriptions, and associated metadata stored in the Travel_Data dictionaries

### Requirement 2: Hotel Recommendations

**User Story:** As a traveler, I want to find hotels at my chosen destination, so that I can book suitable accommodation.

#### Acceptance Criteria

1. WHEN a user requests hotel recommendations for a destination, THE Agent SHALL return hotels available at that destination from the Travel_Data
2. WHEN a user provides a budget amount, THE Agent SHALL filter hotel results to only include hotels with a price per night at or below the specified budget amount
3. THE Hotel Tool SHALL return hotel name, price per night, and rating for each matching result
4. IF no hotels match the specified budget for a destination, THEN THE Agent SHALL inform the user that no hotels are available within their budget and suggest the nearest available price options

### Requirement 3: Restaurant Recommendations

**User Story:** As a traveler, I want to discover restaurants at my destination, so that I can plan my dining experiences.

#### Acceptance Criteria

1. WHEN a user requests restaurant recommendations for a destination, THE Agent SHALL return restaurants available at that destination from the Travel_Data
2. WHEN a user specifies a cuisine preference, THE Agent SHALL filter restaurant results to match the specified cuisine type
3. WHEN a user provides a budget amount for dining, THE Agent SHALL filter restaurant results to only include restaurants within the specified price range
4. THE Restaurant Tool SHALL return restaurant name, cuisine type, and price range for each matching result

### Requirement 4: Activity Recommendations

**User Story:** As a traveler, I want to discover activities and experiences at my destination, so that I can plan an engaging trip.

#### Acceptance Criteria

1. WHEN a user requests activity recommendations for a destination, THE Agent SHALL return activities available at that destination from the Travel_Data
2. WHEN a user provides a budget amount for activities, THE Agent SHALL filter activity results to only include activities with a cost at or below the specified budget amount
3. THE Activity Tool SHALL return activity name, description, and cost for each matching result
4. IF no activities match the specified budget for a destination, THEN THE Agent SHALL inform the user that no activities are available within their budget and suggest the nearest available cost options

### Requirement 5: Budget-Based Trip Planning

**User Story:** As a traveler, I want to plan a complete trip within my total budget, so that I can manage my travel expenses effectively.

#### Acceptance Criteria

1. WHEN a user provides a total trip budget, THE Agent SHALL recommend combinations of hotels, restaurants, and activities that fit within the specified dollar amount
2. THE Agent SHALL calculate the total estimated cost of recommended combinations and present the total to the user
3. WHEN the Agent presents a trip plan, THE Agent SHALL break down costs by category (accommodation, dining, activities)
4. IF no complete trip combination fits within the specified budget, THEN THE Agent SHALL inform the user of the minimum budget required and suggest partial plans within their budget

### Requirement 6: Conversation Memory

**User Story:** As a traveler, I want the agent to remember my preferences during our conversation, so that I do not have to repeat information.

#### Acceptance Criteria

1. THE Session_Memory SHALL maintain user preferences and context throughout a single conversation session
2. WHEN a user has previously stated a destination preference in the session, THE Agent SHALL use that preference in subsequent recommendations without requiring the user to repeat the destination
3. WHEN a user has previously stated a budget in the session, THE Agent SHALL apply that budget to subsequent queries unless the user provides a new budget amount
4. THE Agent SHALL use the Strands manage_conversation_history pattern to persist conversation context within the session

### Requirement 7: Tool Architecture

**User Story:** As a developer, I want the tools to be modular Python functions, so that the agent capabilities are maintainable and extensible.

#### Acceptance Criteria

1. THE Tool modules SHALL use the Strands `@tool` decorator to define each travel data access function
2. THE Tool modules SHALL be implemented as separate Python files importable by the Notebook
3. THE Agent SHALL be configured to use Amazon Bedrock with Claude Sonnet as the model provider
4. THE Notebook SHALL contain sections for setup, tool definitions, agent creation, and interactive demo in sequential order

### Requirement 8: Travel Data Structure

**User Story:** As a developer, I want the travel data to be structured as Python dictionaries, so that the data is easy to maintain and extend.

#### Acceptance Criteria

1. THE Travel_Data SHALL contain at least 5 distinct Egypt destinations
2. THE Travel_Data SHALL include at least 2 hotels per destination with name, price per night, and rating
3. THE Travel_Data SHALL include at least 2 restaurants per destination with name, cuisine type, and price range
4. THE Travel_Data SHALL include at least 2 activities per destination with name, description, and cost
5. THE Travel_Data SHALL store all prices as numeric values in US dollars

### Requirement 9: Interactive Demo

**User Story:** As a user, I want an interactive demo section in the notebook, so that I can test the agent with sample queries.

#### Acceptance Criteria

1. THE Notebook SHALL include an interactive demo section that allows users to input queries and receive agent responses
2. THE Notebook SHALL include example queries demonstrating destination discovery, hotel search, restaurant search, activity search, and budget-based planning
3. WHEN the demo section is executed, THE Agent SHALL respond to user input in natural conversational language
