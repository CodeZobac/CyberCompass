# Error Handling and Graceful Degradation Guide

This guide explains how to use the error handling and graceful degradation systems in the AI Backend.

## Overview

The error handling system consists of three main components:

1. **Custom Exceptions** (`utils/exceptions.py`) - Structured error types with recovery suggestions
2. **Error Handler** (`utils/error_handler.py`) - Logging, monitoring, and middleware
3. **Fallback Service** (`services/fallback_service.py`) - Static educational content
4. **Health Monitor** (`services/health_monitor.py`) - Service health tracking and recovery
5. **Graceful Degradation** (`services/graceful_degradation.py`) - Automatic fallback integration

## Using Custom Exceptions

### Raising Exceptions

```python
from src.utils.exceptions import (
    ValidationError,
    AIServiceError,
    AgentUnavailableError,
    InvalidLocaleError
)

# Validation error
if locale not in ["en", "pt"]:
    raise InvalidLocaleError(locale)

# AI service error
if not agent_available:
    raise AgentUnavailableError("ethics_mentor")

# Generic AI error with details
raise AIServiceError(
    message="Failed to generate feedback",
    details={"user_id": user_id, "attempt": 3}
)
```

### Exception Properties

All custom exceptions include:
- `message`: Human-readable error message
- `category`: Error category for classification
- `status_code`: HTTP status code
- `recovery_suggestion`: User-friendly recovery guidance
- `details`: Additional context dictionary

## Error Handling Decorators

### Basic Error Handling

```python
from src.utils.error_handler import with_error_handling

@with_error_handling
async def generate_feedback(user_id: str):
    # Your code here
    # Exceptions are automatically caught and converted to AIServiceError
    pass
```

### Retry Logic

```python
from src.utils.error_handler import with_retry

@with_retry(max_attempts=3, delay=2.0)
async def call_external_api():
    # Automatically retries on DatabaseError or ExternalServiceError
    pass
```

### Error Context

```python
from src.utils.error_handler import ErrorContext

async def process_user_request(user_id: str):
    async with ErrorContext("process_user_request", user_id=user_id):
        # Your code here
        # Errors are automatically logged with context
        pass
```

## Graceful Degradation

### Using Graceful Degradation Service

```python
from src.services.graceful_degradation import graceful_degradation_service

async def get_feedback(user_id: str, locale: str = "en"):
    # Define your AI function
    async def ai_feedback():
        # AI generation logic
        return await crew.generate_feedback(user_id)
    
    # Automatically falls back to static content on failure
    result = await graceful_degradation_service.get_feedback_with_fallback(
        ai_feedback_func=ai_feedback,
        locale=locale,
        challenge_type="privacy"
    )
    
    # Result includes is_fallback flag
    if result.get("is_fallback"):
        logger.info("Using fallback content")
    
    return result
```

### Using Decorator

```python
from src.services.graceful_degradation import with_graceful_degradation
from src.services.fallback_service import FallbackContentType

@with_graceful_degradation(FallbackContentType.FEEDBACK)
async def generate_feedback(user_id: str, locale: str = "en"):
    # AI generation logic
    # Automatically falls back on AIServiceError
    pass
```

## Health Monitoring

### Registering Services

```python
from src.services.health_monitor import health_monitor

async def check_crewai_health() -> bool:
    """Check if CrewAI agents are responsive."""
    try:
        # Perform health check
        return await crew_manager.ping()
    except Exception:
        return False

async def recover_crewai():
    """Attempt to recover CrewAI service."""
    await crew_manager.restart_agents()

# Register service
health_monitor.register_service(
    service_name="ai_feedback",
    health_check=check_crewai_health,
    recovery_callback=recover_crewai
)

# Start monitoring
await health_monitor.start_monitoring(check_interval=30)
```

### Checking Service Status

```python
from src.services.health_monitor import health_monitor, ServiceStatus

# Check if service is available
if health_monitor.is_service_available("ai_feedback"):
    result = await generate_ai_feedback()
else:
    result = get_fallback_feedback()

# Get detailed health report
health_report = health_monitor.get_health_report()
```

## FastAPI Integration

### Adding Error Handler Middleware

```python
from fastapi import FastAPI
from src.utils.error_handler import error_handler_middleware

app = FastAPI()

# Add error handling middleware
error_handler_middleware(app)
```

### Health Check Endpoint

```python
from fastapi import APIRouter
from src.services.health_monitor import health_monitor
from src.utils.error_handler import health_checker

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return health_checker.get_health_status()

@router.get("/health/detailed")
async def detailed_health():
    """Detailed health report."""
    return health_monitor.get_health_report()
```

### Error Statistics Endpoint

```python
from src.utils.error_handler import error_monitor
from src.services.graceful_degradation import graceful_degradation_service

@router.get("/stats/errors")
async def error_statistics():
    """Get error statistics."""
    return error_monitor.get_error_stats()

@router.get("/stats/degradation")
async def degradation_statistics():
    """Get graceful degradation statistics."""
    return graceful_degradation_service.get_degradation_stats()
```

## Fallback Content

### Available Fallback Types

- `FEEDBACK` - Educational feedback on ethical decisions
- `DEEPFAKE_CHALLENGE` - Deepfake detection challenges
- `SOCIAL_MEDIA_POST` - Social media simulation posts
- `CATFISH_RESPONSE` - Catfish chat responses
- `ANALYTICS` - Analytics messages

### Direct Fallback Access

```python
from src.services.fallback_service import fallback_service

# Get fallback feedback
feedback = fallback_service.get_fallback_feedback(
    locale="en",
    challenge_type="privacy"
)

# Get fallback deepfake challenge
challenge = fallback_service.get_fallback_deepfake_challenge(locale="pt")

# Get fallback catfish response
response = fallback_service.get_fallback_catfish_response(
    user_message="Hey, how are you?",
    locale="en"
)
```

## Best Practices

1. **Always use custom exceptions** instead of generic Python exceptions
2. **Add error handling decorators** to all async functions that might fail
3. **Register services** with health monitor for automatic recovery
4. **Use graceful degradation** for all AI-powered features
5. **Log errors with context** using structured logging
6. **Monitor fallback usage** to identify persistent issues
7. **Test error scenarios** to ensure fallback content is appropriate

## Example: Complete Implementation

```python
from fastapi import APIRouter, Depends
from src.utils.exceptions import ValidationError, InvalidLocaleError
from src.utils.error_handler import with_error_handling, ErrorContext
from src.services.graceful_degradation import graceful_degradation_service

router = APIRouter()

@router.post("/feedback")
@with_error_handling
async def generate_feedback_endpoint(
    user_id: str,
    challenge_id: str,
    locale: str = "en"
):
    """Generate feedback with graceful degradation."""
    
    # Validate input
    if locale not in ["en", "pt"]:
        raise InvalidLocaleError(locale)
    
    async with ErrorContext("generate_feedback", user_id=user_id):
        # Define AI function
        async def ai_feedback():
            return await crew_manager.generate_feedback(
                user_id=user_id,
                challenge_id=challenge_id,
                locale=locale
            )
        
        # Get feedback with automatic fallback
        result = await graceful_degradation_service.get_feedback_with_fallback(
            ai_feedback_func=ai_feedback,
            locale=locale,
            challenge_type="general"
        )
        
        return {
            "success": True,
            "feedback": result,
            "using_fallback": result.get("is_fallback", False)
        }
```

## Monitoring and Alerts

### Error Rate Monitoring

The error monitor automatically tracks error rates and logs warnings when thresholds are exceeded:

```python
# Errors are automatically recorded
# Alert logged when same error occurs > 10 times
```

### Circuit Breaker

Circuit breakers prevent cascading failures:

- **Closed**: Normal operation
- **Open**: Service blocked after 5 failures
- **Half-Open**: Testing recovery after 60 seconds

### Health Check Integration

```python
# Health checks run every 30 seconds (configurable)
# Automatic recovery attempts on failure
# Circuit breakers protect against cascading failures
```

## Testing Error Handling

```python
import pytest
from src.utils.exceptions import AIServiceError
from src.services.graceful_degradation import graceful_degradation_service

@pytest.mark.asyncio
async def test_graceful_degradation():
    """Test fallback when AI service fails."""
    
    async def failing_ai_function():
        raise AIServiceError("Service unavailable")
    
    result = await graceful_degradation_service.get_feedback_with_fallback(
        ai_feedback_func=failing_ai_function,
        locale="en"
    )
    
    assert result["is_fallback"] is True
    assert "feedback" in result
```
