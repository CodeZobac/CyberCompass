"""Cultural content API routes."""

from typing import List
from fastapi import APIRouter, Request, Query

from src.models.requests import DisinformationType
from src.api.middleware.language import (
    get_request_locale,
    get_request_cultural_context
)
from src.services.cultural_content_service import get_cultural_content_service
from src.utils.cultural_agent_helper import get_cultural_agent_helper

router = APIRouter(prefix="/cultural-content", tags=["cultural-content"])


@router.get("/examples/{topic}")
async def get_cultural_examples(
    request: Request,
    topic: str,
    count: int = Query(default=3, ge=1, le=10)
):
    """
    Get culturally-appropriate examples for a topic.
    
    Args:
        request: FastAPI request (contains locale/cultural context)
        topic: Topic for examples
        count: Number of examples to return
        
    Returns:
        List of culturally-appropriate examples
    """
    cultural_context = get_request_cultural_context(request)
    content_service = get_cultural_content_service()
    
    examples = content_service.get_cultural_examples(
        cultural_context, topic, count
    )
    
    return {
        "topic": topic,
        "cultural_context": cultural_context.value,
        "examples": examples
    }


@router.get("/disinformation-patterns/{disinformation_type}")
async def get_disinformation_patterns(
    request: Request,
    disinformation_type: DisinformationType
):
    """
    Get culturally-specific disinformation patterns.
    
    Args:
        request: FastAPI request
        disinformation_type: Type of disinformation
        
    Returns:
        Disinformation patterns for the cultural context
    """
    cultural_context = get_request_cultural_context(request)
    content_service = get_cultural_content_service()
    
    patterns = content_service.get_disinformation_patterns(
        cultural_context, disinformation_type
    )
    
    return {
        "disinformation_type": disinformation_type.value,
        "cultural_context": cultural_context.value,
        "patterns": patterns
    }



@router.get("/scenario/{scenario_type}")
async def generate_scenario(
    request: Request,
    scenario_type: str,
    difficulty: int = Query(default=1, ge=1, le=5)
):
    """
    Generate culturally-appropriate scenario.
    
    Args:
        request: FastAPI request
        scenario_type: Type of scenario
        difficulty: Difficulty level (1-5)
        
    Returns:
        Generated scenario
    """
    cultural_context = get_request_cultural_context(request)
    content_service = get_cultural_content_service()
    
    scenario = content_service.generate_social_media_scenario(
        cultural_context, scenario_type, difficulty
    )
    
    return {
        "scenario_type": scenario_type,
        "cultural_context": cultural_context.value,
        "difficulty": difficulty,
        "scenario": scenario
    }


@router.get("/concerns")
async def get_localized_concerns(request: Request):
    """
    Get localized disinformation concerns.
    
    Args:
        request: FastAPI request
        
    Returns:
        List of localized concerns
    """
    cultural_context = get_request_cultural_context(request)
    content_service = get_cultural_content_service()
    
    concerns = content_service.get_localized_disinformation_concerns(cultural_context)
    platforms = content_service.get_platform_preferences(cultural_context)
    
    return {
        "cultural_context": cultural_context.value,
        "concerns": concerns,
        "preferred_platforms": platforms
    }


@router.get("/communication-style")
async def get_communication_style(request: Request):
    """
    Get communication style guide for cultural context.
    
    Args:
        request: FastAPI request
        
    Returns:
        Communication style guide
    """
    cultural_context = get_request_cultural_context(request)
    content_service = get_cultural_content_service()
    
    style_guide = content_service.get_communication_style_guide(cultural_context)
    
    return {
        "cultural_context": cultural_context.value,
        "style_guide": style_guide
    }
