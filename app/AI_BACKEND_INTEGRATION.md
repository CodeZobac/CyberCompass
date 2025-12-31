# AI Backend Integration Documentation

## Overview

This document describes the integration between the Next.js frontend and the new Python CrewAI backend service. The integration replaces direct Gemini API calls with calls to a dedicated AI microservice that provides enhanced educational feedback using multi-agent systems.

## Architecture Changes

### Before (Monolithic)
```
Next.js App → Gemini API (Direct)
```

### After (Microservices)
```
Next.js App → Python AI Backend (CrewAI) → Multiple LLMs
            ↓ (fallback)
            → Static Feedback Service
```

## Components Modified

### 1. AI Backend Client (`app/lib/services/ai-backend-client.ts`)

**Purpose**: Service layer for communicating with the Python CrewAI backend

**Key Features**:
- Type-safe API client with TypeScript interfaces
- Automatic timeout handling (30 seconds)
- Connection error detection and reporting
- Singleton pattern for efficient resource usage
- Fallback service for graceful degradation

**API Methods**:
- `generateFeedback()` - Get AI feedback for challenge responses
- `startDeepfakeChallenge()` - Initialize deepfake detection challenges
- `submitDeepfakeResult()` - Submit deepfake detection results
- `startSocialMediaSimulation()` - Start social media simulation
- `getUserAnalytics()` - Get user progress analytics
- `healthCheck()` - Check backend availability
- `isAvailable()` - Boolean check for backend status

### 2. AI Feedback Route (`app/app/api/ai-feedback/route.ts`)

**Changes**:
- ✅ Replaced `generateOllamaResponse()` with `aiBackendClient.generateFeedback()`
- ✅ Added user ID and challenge ID to requests
- ✅ Implemented fallback service for when backend is unavailable
- ✅ Enhanced response format with reasoning and follow-up questions
- ✅ Improved error handling with specific error messages

**Request Format**:
```typescript
{
  user_id: string;           // User or session ID
  challenge_id: string;      // Challenge identifier
  selected_option: string;   // User's selected answer
  correct_option: string;    // Correct answer
  locale: string;            // 'en' or 'pt'
  user_history?: Array;      // Optional user history
  context?: {                // Additional context
    challenge_title: string;
    challenge_description: string;
    is_correct: boolean;
  };
}
```

**Response Format**:
```typescript
{
  feedback: string;                    // Main feedback text
  reasoning?: string;                  // Explanation of reasoning
  learning_objectives?: string[];      // Learning goals
  follow_up_questions?: string[];      // Questions for reflection
  confidence_score?: number;           // AI confidence (0-1)
  fallback?: boolean;                  // True if using fallback
  error_message?: string;              // Error details if fallback
}
```

### 3. AI Feedback Component (`app/app/components/AIFeedback.tsx`)

**Changes**:
- ✅ Added user ID from localStorage (session-based)
- ✅ Increased timeout to 30 seconds for AI processing
- ✅ Added fallback indicator UI ("Basic Mode" badge)
- ✅ Display follow-up questions when available
- ✅ Improved error messages (warnings instead of errors)
- ✅ Better loading states and retry functionality

**New UI Features**:
- "Basic Mode" badge when using fallback
- Follow-up questions section with thinking prompts
- Amber warning messages instead of red errors
- Graceful degradation messaging

### 4. Environment Configuration (`app/.env.example`)

**New Variable**:
```bash
NEXT_PUBLIC_AI_BACKEND_URL=http://localhost:8000
```

**Note**: The `NEXT_PUBLIC_` prefix makes this variable available in the browser, which is required for client-side API calls.

## Error Handling Strategy

### 1. Connection Errors
**Scenario**: AI backend is not running or unreachable

**Handling**:
- Catch connection errors in API route
- Log warning (not error) to console
- Use `FallbackService.generateFallbackFeedback()`
- Return response with `fallback: true` flag
- Display "Basic Mode" indicator to user

### 2. Timeout Errors
**Scenario**: AI backend takes too long to respond (>30s)

**Handling**:
- AbortSignal timeout triggers
- Fallback to static feedback
- User sees warning message with retry option
- No application crash or blocking

### 3. Invalid Response Errors
**Scenario**: Backend returns unexpected format

**Handling**:
- JSON parsing errors caught
- Fallback service activated
- User receives basic feedback
- Error logged for debugging

### 4. Rate Limiting
**Scenario**: Too many requests to backend

**Handling**:
- Backend returns 429 status
- Frontend shows appropriate message
- Retry button available
- Fallback service as last resort

## Fallback Service

The `FallbackService` provides basic educational feedback when the AI backend is unavailable:

**Features**:
- Multilingual support (EN/PT)
- Correct/incorrect answer detection
- Educational messaging
- Lower confidence score (0.5) to indicate basic mode
- No external dependencies

**Example Fallback Feedback**:
```
English (Incorrect):
"The correct answer is 'Use a strong, unique password'. Understanding 
the difference between your selected answer and the correct one will 
help deepen your cybersecurity knowledge."

Portuguese (Incorrect):
"A resposta correta é 'Use a strong, unique password'. Compreender a 
diferença entre sua resposta selecionada e a correta ajudará a 
aprofundar seu conhecimento em cibersegurança."
```

## Testing

### Manual Testing Steps

1. **Test with AI Backend Running**:
   ```bash
   # Terminal 1: Start AI backend
   cd ai-backend
   make run
   
   # Terminal 2: Start Next.js
   cd app
   npm run dev
   ```
   - Answer a challenge question
   - Verify enhanced feedback appears
   - Check for follow-up questions
   - No "Basic Mode" badge should appear

2. **Test with AI Backend Stopped**:
   ```bash
   # Stop AI backend (Ctrl+C)
   # Keep Next.js running
   ```
   - Answer a challenge question
   - Verify fallback feedback appears
   - Check for "Basic Mode" badge
   - Verify warning message appears
   - Test retry button

3. **Test Timeout Handling**:
   - Simulate slow backend response
   - Verify 30-second timeout works
   - Check fallback activation

### Automated Testing

Run the integration test script:
```bash
cd app
node test-ai-backend.js
```

This script verifies:
- Backend connectivity
- Request/response structure
- Fallback service functionality
- Environment configuration

## Deployment Considerations

### Environment Variables

**Development**:
```bash
NEXT_PUBLIC_AI_BACKEND_URL=http://localhost:8000
```

**Production**:
```bash
NEXT_PUBLIC_AI_BACKEND_URL=https://ai-backend.cybercompass.app
```

### Docker Compose

Update `docker-compose.yml` to include both services:
```yaml
services:
  frontend:
    build: ./app
    environment:
      - NEXT_PUBLIC_AI_BACKEND_URL=http://ai-backend:8000
    depends_on:
      - ai-backend
  
  ai-backend:
    build: ./ai-backend
    ports:
      - "8000:8000"
```

### Health Checks

The frontend automatically checks backend health:
- On first request, attempts to connect
- If connection fails, uses fallback
- Retry button allows manual reconnection attempts
- No blocking or application crashes

## Migration Path

### Phase 1: Parallel Operation (Current)
- Both Gemini direct calls and AI backend supported
- Gradual rollout to users
- Fallback ensures continuity

### Phase 2: AI Backend Primary
- AI backend becomes primary source
- Gemini used only as fallback
- Monitor performance and user feedback

### Phase 3: Full Migration
- Remove direct Gemini integration
- AI backend only (with static fallback)
- Deprecate old code

## Monitoring and Debugging

### Frontend Logs
```javascript
// Check browser console for:
console.warn('AI backend unavailable, using fallback:', error);
console.log('Using fallback feedback:', data.error_message);
```

### Backend Logs
```python
# Check AI backend logs for:
logger.info(f"Feedback request from user {user_id}")
logger.error(f"CrewAI error: {error}")
```

### Key Metrics to Monitor
- Backend response times
- Fallback usage rate
- Error rates by type
- User satisfaction with feedback quality

## Troubleshooting

### Issue: "Could not connect to the AI service"

**Causes**:
- AI backend not running
- Wrong URL in environment variable
- Network/firewall issues
- Port 8000 not accessible

**Solutions**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check environment variable: `echo $NEXT_PUBLIC_AI_BACKEND_URL`
3. Check Docker network if using containers
4. Verify firewall allows port 8000

### Issue: "Request timeout"

**Causes**:
- AI backend processing too slowly
- Large user history data
- LLM API rate limits

**Solutions**:
1. Check backend logs for bottlenecks
2. Optimize CrewAI agent configurations
3. Increase timeout if needed (currently 30s)
4. Implement request queuing

### Issue: Fallback always used

**Causes**:
- Backend URL incorrect
- Backend returning errors
- Authentication issues

**Solutions**:
1. Test backend directly: `curl http://localhost:8000/health`
2. Check backend logs for errors
3. Verify API endpoint paths match
4. Test with Postman/curl first

## Future Enhancements

### Planned Features
- [ ] WebSocket support for real-time chat simulations
- [ ] Streaming responses for longer feedback
- [ ] Caching layer for common questions
- [ ] A/B testing framework for feedback quality
- [ ] User preference for feedback detail level

### Performance Optimizations
- [ ] Request batching for multiple challenges
- [ ] Response caching with Redis
- [ ] CDN for static fallback content
- [ ] Load balancing for multiple backend instances

## References

- [CrewAI Documentation](https://docs.crewai.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js API Routes](https://nextjs.org/docs/api-routes/introduction)
- [AI Backend Design Document](../../.kiro/specs/ai-backend-separation/design.md)
- [AI Backend Requirements](../../.kiro/specs/ai-backend-separation/requirements.md)
