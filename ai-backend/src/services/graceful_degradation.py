"""
Graceful degradation service integrating error handling and fallback systems.

This module provides a unified interface for handling AI service failures
with automatic fallback to static content and recovery mechanisms.
"""

from typing import Dict, Any, Optional, Callable
from functools import wraps

from ..utils.exceptions import AIServiceError, AgentUnavailableError
from ..utils.error_handler import logger, with_error_handling, with_retry
from .fallback_service import fallback_service, FallbackContentType
from .health_monitor import health_monitor, ServiceStatus


class GracefulDegradationService:
    """
    Service providing graceful degradation for AI functionality.
    
    This service automatically falls back to static content when AI services
    fail and implements recovery strategies to restore full functionality.
    """
    
    def __init__(self):
        self.fallback_service = fallback_service
        self.health_monitor = health_monitor
        self.fallback_usage_count = 0
    
    async def get_feedback_with_fallback(
        self,
        ai_feedback_func: Callable,
        locale: str = "en",
        challenge_type: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get AI feedback with automatic fallback to static content.
        
        Args:
            ai_feedback_func: Async function to generate AI feedback
            locale: Language locale
            challenge_type: Optional challenge type
            **kwargs: Additional arguments for AI function
        
        Returns:
            Feedback response (AI-generated or fallback)
        """
        try:
            # Check if AI service is available
            if not self.health_monitor.is_service_available("ai_feedback"):
                logger.warning("AI feedback service unavailable, using fallback")
                return self._get_fallback_feedback(locale, challenge_type)
            
            # Attempt AI generation
            result = await ai_feedback_func(**kwargs)
            return result
            
        except (AIServiceError, AgentUnavailableError) as e:
            logger.warning(
                "AI feedback generation failed, using fallback",
                error=str(e)
            )
            self.fallback_usage_count += 1
            return self._get_fallback_feedback(locale, challenge_type)
        except Exception as e:
            logger.exception("Unexpected error in feedback generation", exc=e)
            return self._get_fallback_feedback(locale, challenge_type)
    
    async def get_deepfake_challenge_with_fallback(
        self,
        ai_challenge_func: Callable,
        locale: str = "en",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get deepfake challenge with automatic fallback.
        
        Args:
            ai_challenge_func: Async function to generate AI challenge
            locale: Language locale
            **kwargs: Additional arguments for AI function
        
        Returns:
            Challenge response (AI-generated or fallback)
        """
        try:
            if not self.health_monitor.is_service_available("deepfake_challenge"):
                logger.warning("Deepfake challenge service unavailable, using fallback")
                return self._get_fallback_deepfake_challenge(locale)
            
            result = await ai_challenge_func(**kwargs)
            return result
            
        except (AIServiceError, AgentUnavailableError) as e:
            logger.warning(
                "Deepfake challenge generation failed, using fallback",
                error=str(e)
            )
            self.fallback_usage_count += 1
            return self._get_fallback_deepfake_challenge(locale)
        except Exception as e:
            logger.exception("Unexpected error in challenge generation", exc=e)
            return self._get_fallback_deepfake_challenge(locale)
    
    async def get_social_media_post_with_fallback(
        self,
        ai_post_func: Callable,
        locale: str = "en",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get social media post with automatic fallback.
        
        Args:
            ai_post_func: Async function to generate AI post
            locale: Language locale
            **kwargs: Additional arguments for AI function
        
        Returns:
            Post response (AI-generated or fallback)
        """
        try:
            if not self.health_monitor.is_service_available("social_media_sim"):
                logger.warning("Social media service unavailable, using fallback")
                return self._get_fallback_social_media_post(locale)
            
            result = await ai_post_func(**kwargs)
            return result
            
        except (AIServiceError, AgentUnavailableError) as e:
            logger.warning(
                "Social media post generation failed, using fallback",
                error=str(e)
            )
            self.fallback_usage_count += 1
            return self._get_fallback_social_media_post(locale)
        except Exception as e:
            logger.exception("Unexpected error in post generation", exc=e)
            return self._get_fallback_social_media_post(locale)
    
    async def get_catfish_response_with_fallback(
        self,
        ai_response_func: Callable,
        user_message: str,
        locale: str = "en",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get catfish response with automatic fallback.
        
        Args:
            ai_response_func: Async function to generate AI response
            user_message: User's message
            locale: Language locale
            **kwargs: Additional arguments for AI function
        
        Returns:
            Response (AI-generated or fallback)
        """
        try:
            if not self.health_monitor.is_service_available("catfish_chat"):
                logger.warning("Catfish chat service unavailable, using fallback")
                return self._get_fallback_catfish_response(user_message, locale)
            
            result = await ai_response_func(user_message=user_message, **kwargs)
            return result
            
        except (AIServiceError, AgentUnavailableError) as e:
            logger.warning(
                "Catfish response generation failed, using fallback",
                error=str(e)
            )
            self.fallback_usage_count += 1
            return self._get_fallback_catfish_response(user_message, locale)
        except Exception as e:
            logger.exception("Unexpected error in response generation", exc=e)
            return self._get_fallback_catfish_response(user_message, locale)
    
    async def get_analytics_with_fallback(
        self,
        ai_analytics_func: Callable,
        locale: str = "en",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get analytics with automatic fallback.
        
        Args:
            ai_analytics_func: Async function to generate AI analytics
            locale: Language locale
            **kwargs: Additional arguments for AI function
        
        Returns:
            Analytics response (AI-generated or fallback)
        """
        try:
            if not self.health_monitor.is_service_available("analytics"):
                logger.warning("Analytics service unavailable, using fallback")
                return self._get_fallback_analytics(locale)
            
            result = await ai_analytics_func(**kwargs)
            return result
            
        except (AIServiceError, AgentUnavailableError) as e:
            logger.warning(
                "Analytics generation failed, using fallback",
                error=str(e)
            )
            self.fallback_usage_count += 1
            return self._get_fallback_analytics(locale)
        except Exception as e:
            logger.exception("Unexpected error in analytics generation", exc=e)
            return self._get_fallback_analytics(locale)
    
    def _get_fallback_feedback(
        self,
        locale: str,
        challenge_type: Optional[str]
    ) -> Dict[str, Any]:
        """Get fallback feedback from fallback service."""
        return self.fallback_service.get_fallback_feedback(locale, challenge_type)
    
    def _get_fallback_deepfake_challenge(self, locale: str) -> Dict[str, Any]:
        """Get fallback deepfake challenge from fallback service."""
        return self.fallback_service.get_fallback_deepfake_challenge(locale)
    
    def _get_fallback_social_media_post(self, locale: str) -> Dict[str, Any]:
        """Get fallback social media post from fallback service."""
        return self.fallback_service.get_fallback_social_media_post(locale)
    
    def _get_fallback_catfish_response(
        self,
        user_message: str,
        locale: str
    ) -> Dict[str, Any]:
        """Get fallback catfish response from fallback service."""
        return self.fallback_service.get_fallback_catfish_response(user_message, locale)
    
    def _get_fallback_analytics(self, locale: str) -> Dict[str, Any]:
        """Get fallback analytics from fallback service."""
        return self.fallback_service.get_fallback_analytics(locale)
    
    def get_degradation_stats(self) -> Dict[str, Any]:
        """Get statistics about graceful degradation usage."""
        return {
            "fallback_usage_count": self.fallback_usage_count,
            "fallback_service_stats": self.fallback_service.get_usage_statistics(),
            "health_report": self.health_monitor.get_health_report()
        }


# Global graceful degradation service instance
graceful_degradation_service = GracefulDegradationService()


def with_graceful_degradation(fallback_type: FallbackContentType, locale_param: str = "locale"):
    """
    Decorator to add graceful degradation to AI functions.
    
    Args:
        fallback_type: Type of fallback content to use
        locale_param: Name of the locale parameter in the function
    
    Usage:
        @with_graceful_degradation(FallbackContentType.FEEDBACK)
        async def generate_feedback(user_id: str, locale: str = "en"):
            # AI generation code
    """
    
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            locale = kwargs.get(locale_param, "en")
            
            try:
                return await func(*args, **kwargs)
            except (AIServiceError, AgentUnavailableError) as e:
                logger.warning(
                    f"AI function {func.__name__} failed, using fallback",
                    error=str(e),
                    fallback_type=fallback_type.value
                )
                
                # Get appropriate fallback based on type
                if fallback_type == FallbackContentType.FEEDBACK:
                    return fallback_service.get_fallback_feedback(locale)
                elif fallback_type == FallbackContentType.DEEPFAKE_CHALLENGE:
                    return fallback_service.get_fallback_deepfake_challenge(locale)
                elif fallback_type == FallbackContentType.SOCIAL_MEDIA_POST:
                    return fallback_service.get_fallback_social_media_post(locale)
                elif fallback_type == FallbackContentType.ANALYTICS:
                    return fallback_service.get_fallback_analytics(locale)
                else:
                    raise
        
        return wrapper
    
    return decorator
