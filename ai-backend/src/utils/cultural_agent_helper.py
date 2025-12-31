"""Helper utilities for culturally-aware agent responses."""

from typing import Dict, Optional
from fastapi import Request

from src.models.requests import LocaleEnum, DisinformationType
from src.services.language_service import get_language_service, CulturalContext
from src.services.cultural_content_service import get_cultural_content_service
from src.api.middleware.language import (
    get_request_locale,
    get_request_cultural_context,
    get_language_routing_config
)


class CulturalAgentHelper:
    """Helper class for building culturally-aware agent prompts and responses."""
    
    def __init__(self):
        """Initialize cultural agent helper."""
        self.language_service = get_language_service()
        self.content_service = get_cultural_content_service()
    
    def build_culturally_aware_prompt(
        self,
        base_prompt: str,
        locale: LocaleEnum,
        cultural_context: CulturalContext,
        topic: Optional[str] = None,
        include_examples: bool = True
    ) -> str:
        """
        Build a culturally-aware prompt for an agent.
        
        Args:
            base_prompt: Base agent prompt
            locale: User locale
            cultural_context: Cultural context
            topic: Optional topic for examples
            include_examples: Whether to include cultural examples
            
        Returns:
            Enhanced prompt with cultural adaptation
        """
        # Get language routing config
        routing_config = self.language_service.get_agent_routing_config(
            locale, cultural_context
        )
        
        # Build enhanced prompt
        enhanced_prompt = self.language_service.adapt_agent_prompt(
            base_prompt, locale, cultural_context
        )
        
        # Add cultural examples if requested
        if include_examples and topic:
            examples = self.content_service.get_cultural_examples(
                cultural_context, topic, count=3
            )
            
            if examples:
                examples_text = "\n".join([f"- {ex}" for ex in examples])
                enhanced_prompt += f"\n\nCULTURAL EXAMPLES FOR {topic.upper()}:\n{examples_text}\n"
        
        # Add platform preferences
        platforms = self.content_service.get_platform_preferences(cultural_context)
        enhanced_prompt += f"\n\nPREFERRED PLATFORMS: {', '.join(platforms[:3])}\n"
        
        # Add localized concerns
        concerns = self.content_service.get_localized_disinformation_concerns(cultural_context)
        concerns_text = "\n".join([f"- {concern}" for concern in concerns])
        enhanced_prompt += f"\n\nLOCALIZED CONCERNS:\n{concerns_text}\n"
        
        return enhanced_prompt
    
    def get_disinformation_context(
        self,
        cultural_context: CulturalContext,
        disinformation_type: DisinformationType
    ) -> Dict:
        """
        Get culturally-specific disinformation context.
        
        Args:
            cultural_context: Cultural context
            disinformation_type: Type of disinformation
            
        Returns:
            Dictionary with disinformation patterns and context
        """
        return self.content_service.get_disinformation_patterns(
            cultural_context, disinformation_type
        )
    
    def generate_culturally_appropriate_scenario(
        self,
        cultural_context: CulturalContext,
        scenario_type: str,
        difficulty: int = 1
    ) -> Dict:
        """
        Generate a culturally-appropriate educational scenario.
        
        Args:
            cultural_context: Cultural context
            scenario_type: Type of scenario
            difficulty: Difficulty level
            
        Returns:
            Scenario dictionary
        """
        return self.content_service.generate_social_media_scenario(
            cultural_context, scenario_type, difficulty
        )
    
    def extract_cultural_context_from_request(self, request: Request) -> Dict:
        """
        Extract all cultural context information from a request.
        
        Args:
            request: FastAPI request object
            
        Returns:
            Dictionary with locale, cultural context, and routing config
        """
        return {
            "locale": get_request_locale(request),
            "cultural_context": get_request_cultural_context(request),
            "routing_config": get_language_routing_config(request)
        }


# Singleton instance
_cultural_agent_helper: Optional[CulturalAgentHelper] = None


def get_cultural_agent_helper() -> CulturalAgentHelper:
    """Get singleton instance of cultural agent helper."""
    global _cultural_agent_helper
    if _cultural_agent_helper is None:
        _cultural_agent_helper = CulturalAgentHelper()
    return _cultural_agent_helper
