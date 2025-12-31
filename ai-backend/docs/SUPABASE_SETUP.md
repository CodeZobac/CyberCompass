# Supabase Integration Setup

## Overview
This document describes the Supabase integration for the AI Backend, including database schema, data access layer, and usage examples.

## Database Schema

### Tables Created

#### 1. `ai_user_sessions`
Tracks AI interaction sessions for users.

**Columns:**
- `id` (UUID, PK): Unique session identifier
- `user_id` (UUID, FK → users.id): Reference to user
- `session_id` (TEXT, UNIQUE): Session identifier string
- `activity_type` (TEXT): Type of activity (deepfake_detection, social_media_sim, catfish_chat, ethics_feedback, analytics)
- `start_time` (TIMESTAMPTZ): Session start time
- `end_time` (TIMESTAMPTZ, nullable): Session end time
- `context` (JSONB): Session context data
- `flow_state` (JSONB): Current flow state
- `created_at` (TIMESTAMPTZ): Record creation time
- `updated_at` (TIMESTAMPTZ): Last update time

**Indexes:**
- `idx_ai_user_sessions_user_id`
- `idx_ai_user_sessions_session_id`
- `idx_ai_user_sessions_activity_type`
- `idx_ai_user_sessions_start_time`

#### 2. `ai_conversations`
Stores chat history and conversation data.

**Columns:**
- `id` (UUID, PK): Unique conversation identifier
- `user_id` (UUID, FK → users.id): Reference to user
- `session_id` (TEXT, FK → ai_user_sessions.session_id): Reference to session
- `scenario_type` (TEXT): Scenario type (catfish_detection, social_media_sim, deepfake_analysis, ethics_discussion)
- `messages` (JSONB): Array of conversation messages
- `agent_memory` (JSONB): Agent memory state
- `analysis_results` (JSONB, nullable): Analysis results
- `character_profile` (JSONB, nullable): Character profile data
- `red_flags_revealed` (JSONB): Array of revealed red flags
- `created_at` (TIMESTAMPTZ): Record creation time
- `updated_at` (TIMESTAMPTZ): Last update time

**Indexes:**
- `idx_ai_conversations_user_id`
- `idx_ai_conversations_session_id`
- `idx_ai_conversations_scenario_type`
- `idx_ai_conversations_created_at`

#### 3. `ai_challenge_results`
Tracks user performance on challenges.

**Columns:**
- `id` (UUID, PK): Unique result identifier
- `user_id` (UUID, FK → users.id): Reference to user
- `session_id` (TEXT, FK → ai_user_sessions.session_id): Reference to session
- `challenge_type` (TEXT): Challenge type (deepfake_detection, disinformation_identification, catfish_detection, ethics_dilemma)
- `challenge_data` (JSONB): Challenge data
- `user_response` (JSONB): User's response
- `ai_feedback` (JSONB): AI-generated feedback
- `score` (FLOAT, 0-100): Challenge score
- `difficulty_level` (INT, 1-5): Difficulty level
- `time_taken_seconds` (INT, nullable): Time taken to complete
- `created_at` (TIMESTAMPTZ): Record creation time

**Indexes:**
- `idx_ai_challenge_results_user_id`
- `idx_ai_challenge_results_session_id`
- `idx_ai_challenge_results_challenge_type`
- `idx_ai_challenge_results_created_at`

#### 4. `ai_user_analytics`
Stores aggregated user analytics and progress.

**Columns:**
- `id` (UUID, PK): Unique analytics identifier
- `user_id` (UUID, UNIQUE, FK → users.id): Reference to user
- `competency_scores` (JSONB): Competency scores by category
- `progress_trends` (JSONB): Array of progress trend data
- `recommendations` (JSONB): Array of recommendations
- `achievements` (JSONB): Array of achievements
- `total_sessions` (INT): Total number of sessions
- `total_challenges_completed` (INT): Total challenges completed
- `average_score` (FLOAT, nullable): Average challenge score
- `last_activity` (TIMESTAMPTZ, nullable): Last activity timestamp
- `created_at` (TIMESTAMPTZ): Record creation time
- `last_updated` (TIMESTAMPTZ): Last update time

**Indexes:**
- `idx_ai_user_analytics_user_id`
- `idx_ai_user_analytics_last_activity`

### Row Level Security (RLS)

All tables have RLS enabled with the following policies:

1. **Users can view own data**: Users can SELECT their own records
2. **Users can insert own data**: Users can INSERT records for themselves
3. **Users can update own data**: Users can UPDATE their own records (where applicable)
4. **Service role full access**: Service role has full access for backend operations

## Data Access Layer

### Repository Pattern

The data access layer uses the Repository pattern with the following structure:

```
src/repositories/
├── __init__.py
├── base_repository.py          # Base CRUD operations
├── session_repository.py       # Session-specific operations
├── conversation_repository.py  # Conversation-specific operations
├── challenge_repository.py     # Challenge result operations
└── analytics_repository.py     # Analytics operations
```

### Base Repository

`BaseRepository` provides common CRUD operations:
- `create(data)`: Create a new record
- `get_by_id(record_id)`: Get record by ID
- `get_all(limit, offset)`: Get all records with pagination
- `update(record_id, data)`: Update a record
- `delete(record_id)`: Delete a record
- `filter_by(filters, limit, offset)`: Filter records by criteria

### Specialized Repositories

#### SessionRepository
- `get_by_session_id(session_id)`: Get session by session_id
- `get_user_sessions(user_id, activity_type, limit)`: Get user's sessions
- `get_active_sessions(user_id)`: Get active (not ended) sessions

#### ConversationRepository
- `get_by_session_id(session_id)`: Get conversations for a session
- `get_user_conversations(user_id, scenario_type, limit)`: Get user's conversations
- `append_message(conversation_id, message)`: Append message to conversation

#### ChallengeResultRepository
- `get_by_session_id(session_id)`: Get challenge results for a session
- `get_user_results(user_id, challenge_type, limit)`: Get user's challenge results
- `get_user_statistics(user_id, challenge_type)`: Get user statistics

#### AnalyticsRepository
- `get_by_user_id(user_id)`: Get analytics for a user
- `get_or_create(user_id)`: Get or create analytics for a user
- `increment_sessions(user_id)`: Increment session count
- `increment_challenges(user_id, score)`: Increment challenge count and update average

## Usage Examples

### 1. Initialize Supabase Client

```python
from src.database import get_supabase_client

# Get the Supabase client (cached)
supabase = get_supabase_client()
```

### 2. Create a Session

```python
from src.repositories import SessionRepository
from src.models.database import AIUserSessionCreate
from uuid import uuid4

# Initialize repository
session_repo = SessionRepository(supabase)

# Create session data
session_data = AIUserSessionCreate(
    user_id=user_id,
    session_id=str(uuid4()),
    activity_type="catfish_chat",
    context={"language": "en", "difficulty": "medium"}
)

# Create session
session = await session_repo.create(session_data)
```

### 3. Create a Conversation

```python
from src.repositories import ConversationRepository
from src.models.database import AIConversationCreate

# Initialize repository
conv_repo = ConversationRepository(supabase)

# Create conversation data
conv_data = AIConversationCreate(
    user_id=user_id,
    session_id=session.session_id,
    scenario_type="catfish_detection",
    messages=[
        {"role": "assistant", "content": "Hello! Let's start the conversation."}
    ]
)

# Create conversation
conversation = await conv_repo.create(conv_data)
```

### 4. Append Message to Conversation

```python
# Append a user message
new_message = {
    "role": "user",
    "content": "Hi there!",
    "timestamp": datetime.utcnow().isoformat()
}

updated_conv = await conv_repo.append_message(
    conversation.id,
    new_message
)
```

### 5. Save Challenge Result

```python
from src.repositories import ChallengeResultRepository
from src.models.database import AIChallengeResultCreate

# Initialize repository
challenge_repo = ChallengeResultRepository(supabase)

# Create challenge result
result_data = AIChallengeResultCreate(
    user_id=user_id,
    session_id=session.session_id,
    challenge_type="deepfake_detection",
    challenge_data={"image_url": "...", "options": [...]},
    user_response={"selected_option": "real"},
    ai_feedback={"correct": True, "explanation": "..."},
    score=85.0,
    difficulty_level=3,
    time_taken_seconds=45
)

result = await challenge_repo.create(result_data)
```

### 6. Update User Analytics

```python
from src.repositories import AnalyticsRepository

# Initialize repository
analytics_repo = AnalyticsRepository(supabase)

# Increment session count
await analytics_repo.increment_sessions(user_id)

# Increment challenge count with score
await analytics_repo.increment_challenges(user_id, score=85.0)
```

### 7. Get User Statistics

```python
# Get challenge statistics
stats = await challenge_repo.get_user_statistics(
    user_id=user_id,
    challenge_type="deepfake_detection"
)

# Returns:
# {
#     "total_challenges": 10,
#     "average_score": 82.5,
#     "total_time_seconds": 450,
#     "average_time_seconds": 45
# }
```

## Environment Variables

Add the following to your `.env` file:

```env
# Supabase
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-anon-key-here"
SUPABASE_SERVICE_ROLE_KEY="your-service-role-key-here"
```

## Error Handling

All repository methods include error handling and will raise exceptions with descriptive messages:

```python
try:
    session = await session_repo.create(session_data)
except Exception as e:
    print(f"Error creating session: {str(e)}")
```

## Data Validation

All data models use Pydantic for validation:
- Type checking
- Field constraints (e.g., score 0-100, difficulty 1-5)
- Pattern matching for enum-like fields
- Automatic serialization/deserialization

## Next Steps

1. Configure your Supabase credentials in `.env`
2. Install dependencies: `pip install -r requirements.txt`
3. Use the repositories in your API endpoints and services
4. Implement additional business logic as needed
