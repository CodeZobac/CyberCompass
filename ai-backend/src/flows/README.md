# CrewAI Flows for Educational Scenarios

This module contains CrewAI Flow implementations for complex educational scenarios in the Cyber Compass AI Backend.

## Overview

CrewAI Flows provide a structured way to manage complex, multi-step AI interactions. Each flow coordinates multiple agents to deliver sophisticated educational experiences.

## Available Flows

### 1. DeepfakeDetectionFlow

**Purpose**: Train users to detect deepfake content through interactive challenges.

**Features**:
- Generates challenges with appropriate difficulty levels
- Analyzes user submissions with detailed feedback
- Provides detection clues and technical explanations
- Adapts difficulty based on performance
- Supports audio, video, and image content

**Usage**:
```python
from flows import DeepfakeDetectionFlow
from agents.factory import AgentFactory
from models.requests import DeepfakeChallengeRequest, MediaType, LocaleEnum

# Initialize
agent_factory = AgentFactory()
flow = DeepfakeDetectionFlow(agent_factory, locale="en")

# Create challenge
request = DeepfakeChallengeRequest(
    user_id="user_123",
    difficulty_level=2,
    media_type=MediaType.VIDEO,
    locale=LocaleEnum.EN,
)

# Start flow
challenge_state = flow.initialize_challenge(request)
```

**Flow Stages**:
1. `initialize_challenge` - Generate challenge with media content
2. `await_user_submission` - Wait for user's detection decision
3. `process_submission` - Analyze submission and provide feedback
4. `determine_next_action` - Route to difficulty adjustment or training
5. `adapt_difficulty_up/maintain/provide_training` - Adjust experience

**Agents Used**:
- `deepfake_analyst` - Analyzes media and generates challenges
- `ethics_mentor` - Provides educational feedback

### 2. SocialMediaSimulationFlow

**Purpose**: Simulate realistic social media environments with disinformation for detection training.

**Features**:
- Generates mixed authentic and disinformation content
- Tracks user engagement patterns in real-time
- Provides algorithm feedback on content amplification
- Scores detection accuracy
- Analyzes vulnerability to disinformation

**Usage**:
```python
from flows import SocialMediaSimulationFlow
from models.requests import SocialMediaSimulationRequest, DisinformationType

# Initialize
flow = SocialMediaSimulationFlow(agent_factory, locale="en")

# Start simulation
request = SocialMediaSimulationRequest(
    user_id="user_123",
    session_duration_minutes=15,
    disinformation_ratio=0.3,
    categories=[DisinformationType.HEALTH, DisinformationType.POLITICS],
    locale=LocaleEnum.EN,
)

init_state = flow.initialize_simulation(request)

# Track interactions
interaction = flow.record_interaction(
    session_id=init_state['session_id'],
    user_id="user_123",
    post_id=post_id,
    interaction_type="like",  # or "share", "report", "comment"
)
```

**Flow Stages**:
1. `initialize_simulation` - Generate social media feed
2. `track_user_engagement` - Monitor user interactions
3. `record_interaction` - Process each user action with feedback
4. `check_session_status` - Determine if session should continue
5. `analyze_session_performance` - Generate comprehensive analysis

**Agents Used**:
- `social_media_simulator` - Generates realistic content
- `analytics_agent` - Analyzes user behavior
- `ethics_mentor` - Provides educational insights

### 3. CatfishDetectionFlow

**Purpose**: Interactive chat simulation with suspicious personas to teach catfishing detection.

**Features**:
- Creates believable characters with intentional inconsistencies
- Maintains conversation with realistic typing delays
- Strategically reveals red flags through natural dialogue
- Tracks user's detection awareness
- Provides comprehensive safety education

**Usage**:
```python
from flows import CatfishDetectionFlow
from models.requests import CatfishChatStartRequest

# Initialize
flow = CatfishDetectionFlow(agent_factory, locale="en")

# Start chat
request = CatfishChatStartRequest(
    user_id="user_123",
    difficulty_level=2,
    character_age_range="13-17",
    locale=LocaleEnum.EN,
)

char_state = flow.initialize_character(request)
conv_state = flow.start_conversation(char_state)

# Process user messages
response = flow.process_user_message(
    session_id=char_state['session_id'],
    user_id="user_123",
    message_content="Hi! What school do you go to?",
)
```

**Flow Stages**:
1. `initialize_character` - Create catfish character profile
2. `start_conversation` - Send opening message
3. `manage_conversation_flow` - Coordinate ongoing chat
4. `process_user_message` - Generate character responses
5. `check_conversation_status` - Route based on detection progress
6. `_generate_final_analysis` - Provide comprehensive feedback

**Agents Used**:
- `catfish_character` - Simulates suspicious persona
- `conversation_moderator` - Manages conversation flow
- `analytics_agent` - Analyzes detection performance
- `ethics_mentor` - Provides safety education

## Flow Architecture

### CrewAI Flow Decorators

All flows use CrewAI's flow control decorators:

- `@start()` - Entry point of the flow
- `@listen(method)` - Listen for completion of another method
- `@router(method)` - Route to different paths based on conditions

### Memory Systems

Flows integrate with CrewAI's memory systems:

- **Long-term Memory**: Persists character profiles, user history
- **Short-term Memory**: Maintains conversation context
- **Entity Memory**: Tracks specific entities (users, characters)

### State Management

Each flow maintains state through:
- Instance variables for current session data
- Memory systems for persistence
- Flow state dictionaries passed between methods

## Multilingual Support

All flows support English (`en`) and Portuguese (`pt`):

```python
# English flow
flow_en = DeepfakeDetectionFlow(agent_factory, locale="en")

# Portuguese flow
flow_pt = DeepfakeDetectionFlow(agent_factory, locale="pt")
```

Content, feedback, and instructions are automatically adapted to the specified locale.

## Error Handling

Flows include error handling for:
- Invalid session IDs
- Missing challenge data
- Agent failures
- Timeout conditions

Example:
```python
try:
    response = flow.process_user_message(session_id, user_id, message)
except ValueError as e:
    # Handle invalid session or missing data
    print(f"Error: {e}")
```

## Testing

Run the example file to test all flows:

```bash
cd ai-backend
python -m src.flows.flow_examples
```

Or test individual flows:

```python
from flows.flow_examples import FlowExamples
from agents.factory import AgentFactory

agent_factory = AgentFactory()
examples = FlowExamples(agent_factory)

# Test specific flow
results = examples.example_deepfake_detection_flow()
```

## Integration with FastAPI

Flows are designed to integrate with FastAPI endpoints:

```python
from fastapi import FastAPI, WebSocket
from flows import CatfishDetectionFlow

app = FastAPI()
flow = CatfishDetectionFlow(agent_factory)

@app.websocket("/ws/catfish/{session_id}")
async def catfish_chat(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    while True:
        # Receive user message
        message = await websocket.receive_text()
        
        # Process with flow
        response = flow.process_user_message(
            session_id=session_id,
            user_id=user_id,
            message_content=message,
        )
        
        # Send response with typing delay
        await asyncio.sleep(response['typing_delay'])
        await websocket.send_json(response['response'])
```

## Performance Considerations

- **Concurrent Users**: Flows are instance-based; create separate instances per user session
- **Memory Usage**: Long-term memory is persisted; clean up completed sessions
- **Response Times**: Typing delays simulate human behavior (1-5 seconds)
- **Agent Coordination**: Multiple agents may increase processing time

## Best Practices

1. **Session Management**: Always track session IDs and clean up completed sessions
2. **Error Recovery**: Implement graceful degradation for agent failures
3. **User Context**: Provide user history for personalized experiences
4. **Locale Consistency**: Use the same locale throughout a session
5. **Memory Cleanup**: Clear short-term memory at session end

## Requirements

- CrewAI >= 0.28.0
- Python >= 3.10
- OpenAI API key (for LLM access)

## Configuration

Flows use agents defined in `config/agents.yaml`. Customize agent behavior by modifying:
- Agent roles and goals
- LLM models and parameters
- Tools and capabilities
- Memory settings

## Future Enhancements

Planned improvements:
- Async flow execution for better performance
- Flow composition (combining multiple flows)
- Advanced routing with ML-based decisions
- Real-time collaboration between multiple users
- Integration with external deepfake detection APIs

## Support

For issues or questions:
1. Check the flow examples in `flow_examples.py`
2. Review agent configurations in `config/agents.yaml`
3. Consult the main project documentation
4. Review CrewAI documentation: https://docs.crewai.com/

## License

Part of the Cyber Compass AI Backend project.
