# Multilingual Support and Cultural Adaptation

This document describes the multilingual support and cultural adaptation features implemented in the AI backend.

## Overview

The system supports automatic language detection, cultural context adaptation, and culturally-aware content generation for Portuguese (Brazil/Portugal) and English (US/UK) users.

## Features

### 1. Automatic Language Detection

The `LanguageDetectionMiddleware` automatically detects the user's language from:
- Query parameters (`?locale=pt`)
- Request body (JSON with `locale` field)
- `Accept-Language` header
- User preferences (if authenticated)
- Default fallback (English)

### 2. Cultural Context Adaptation

The system identifies cultural variants:
- `en_US` - English (United States)
- `en_UK` - English (United Kingdom)
- `pt_BR` - Portuguese (Brazil)
- `pt_PT` - Portuguese (Portugal)

### 3. Culturally-Aware Content Generation

Content is adapted based on:
- Local social media platforms (e.g., WhatsApp in Brazil)
- Regional disinformation patterns
- Cultural communication styles
- Localized examples and scenarios

## Usage

### In API Routes

```python
from fastapi import Request
from src.api.middleware.language import (
    get_request_locale,
    get_request_cultural_context
)

@router.post("/feedback")
async def generate_feedback(request: Request):
    locale = get_request_locale(request)
    cultural_context = get_request_cultural_context(request)
    
    # Use locale and cultural_context in your logic
    ...
```

### Building Culturally-Aware Agent Prompts

```python
from src.utils.cultural_agent_helper import get_cultural_agent_helper

helper = get_cultural_agent_helper()

# Build enhanced prompt with cultural adaptation
enhanced_prompt = helper.build_culturally_aware_prompt(
    base_prompt="You are an educational AI assistant...",
    locale=LocaleEnum.PT,
    cultural_context=CulturalContext.PORTUGUESE_BRAZIL,
    topic="privacy",
    include_examples=True
)
```

### Getting Cultural Examples

```python
from src.services.cultural_content_service import get_cultural_content_service

content_service = get_cultural_content_service()

# Get examples for a topic
examples = content_service.get_cultural_examples(
    cultural_context=CulturalContext.PORTUGUESE_BRAZIL,
    topic="deepfakes",
    count=3
)
```

### Getting Disinformation Patterns

```python
patterns = content_service.get_disinformation_patterns(
    cultural_context=CulturalContext.PORTUGUESE_BRAZIL,
    disinformation_type=DisinformationType.HEALTH
)
```

## API Endpoints

### Get Cultural Examples
```
GET /api/v1/cultural-content/examples/{topic}?count=3
```

### Get Disinformation Patterns
```
GET /api/v1/cultural-content/disinformation-patterns/{type}
```

### Generate Scenario
```
GET /api/v1/cultural-content/scenario/{type}?difficulty=1
```

### Get Localized Concerns
```
GET /api/v1/cultural-content/concerns
```

### Get Communication Style
```
GET /api/v1/cultural-content/communication-style
```

## Configuration

Supported locales are configured in `config.py`:

```python
supported_locales: str = Field(default="en,pt")
default_locale: str = Field(default="en")
```

## Cultural Content Templates

Content templates are defined in `cultural_content_service.py` and include:

- **Examples**: Platform-specific examples (WhatsApp for Brazil, Twitter for US)
- **Disinformation Patterns**: Regional concerns and red flags
- **Scenarios**: Culturally-appropriate educational scenarios
- **Communication Styles**: Tone, formality, and cultural references

## Testing Language Detection

You can test language detection by:

1. Setting the `Accept-Language` header:
```bash
curl -H "Accept-Language: pt-BR" http://localhost:8000/api/v1/cultural-content/concerns
```

2. Using query parameters:
```bash
curl http://localhost:8000/api/v1/cultural-content/concerns?locale=pt
```

## Extending Support

To add a new language/culture:

1. Add locale to `LocaleEnum` in `models/requests.py`
2. Add cultural context to `CulturalContext` in `language_service.py`
3. Add content templates in `cultural_content_service.py`
4. Update configuration in `config.py`

## Best Practices

1. **Always use the middleware**: The `LanguageDetectionMiddleware` should be included in the app
2. **Access locale from request state**: Use helper functions to get locale/cultural context
3. **Adapt agent prompts**: Use `CulturalAgentHelper` to build culturally-aware prompts
4. **Test with different locales**: Ensure content works across all supported cultures
5. **Respect cultural sensitivities**: Review content templates for cultural appropriateness
