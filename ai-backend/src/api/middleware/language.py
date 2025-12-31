"""Language detection and routing middleware."""

from typing import Callable, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.models.requests import LocaleEnum
from src.services.language_service import get_language_service, CulturalContext


class LanguageDetectionMiddleware(BaseHTTPMiddleware):
    """Middleware to detect and set language context for requests."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and detect language.
        
        Args:
            request: Incoming request
            call_next: Next middleware/handler
            
        Returns:
            Response from handler
        """
        language_service = get_language_service()
        
        # Try to get locale from multiple sources (in order of priority)
        locale = self._get_locale_from_request(request, language_service)
        
        # Get cultural context
        user_preferences = getattr(request.state, "user_preferences", None)
        cultural_context = language_service.get_cultural_context(locale, user_preferences)
        
        # Store in request state for use by handlers
        request.state.locale = locale
        request.state.cultural_context = cultural_context
        request.state.language_routing = language_service.get_agent_routing_config(
            locale, cultural_context
        )
        
        # Process request
        response = await call_next(request)
        
        # Add language headers to response
        response.headers["Content-Language"] = locale.value
        response.headers["X-Cultural-Context"] = cultural_context.value
        
        return response
    
    def _get_locale_from_request(
        self, 
        request: Request, 
        language_service
    ) -> LocaleEnum:
        """
        Extract locale from request using multiple strategies.
        
        Priority order:
        1. Query parameter (?locale=pt)
        2. Request body (if JSON with locale field)
        3. Accept-Language header
        4. User preferences (if authenticated)
        5. Default locale
        
        Args:
            request: Incoming request
            language_service: Language detection service
            
        Returns:
            Detected locale
        """
        # 1. Check query parameter
        locale_param = request.query_params.get("locale")
        if locale_param:
            is_valid, locale_enum = language_service.validate_locale(locale_param)
            if is_valid:
                return locale_enum
        
        # 2. Check if locale is in request state (set by auth middleware)
        if hasattr(request.state, "user_locale"):
            return request.state.user_locale
        
        # 3. Check Accept-Language header
        accept_language = request.headers.get("Accept-Language")
        if accept_language:
            locale = self._parse_accept_language(accept_language, language_service)
            if locale:
                return locale
        
        # 4. Check user preferences (if user is authenticated)
        if hasattr(request.state, "user") and request.state.user:
            user_locale = getattr(request.state.user, "preferred_locale", None)
            if user_locale:
                is_valid, locale_enum = language_service.validate_locale(user_locale)
                if is_valid:
                    return locale_enum
        
        # 5. Default to English
        return LocaleEnum.EN
    
    def _parse_accept_language(
        self, 
        accept_language: str, 
        language_service
    ) -> Optional[LocaleEnum]:
        """
        Parse Accept-Language header.
        
        Format: "en-US,en;q=0.9,pt;q=0.8"
        
        Args:
            accept_language: Accept-Language header value
            language_service: Language detection service
            
        Returns:
            Detected locale or None
        """
        # Split by comma and get language codes
        languages = []
        for lang_entry in accept_language.split(","):
            # Remove quality factor (;q=0.9)
            lang_code = lang_entry.split(";")[0].strip()
            
            # Extract base language (en-US -> en)
            base_lang = lang_code.split("-")[0].lower()
            
            languages.append(base_lang)
        
        # Try each language in order
        for lang in languages:
            is_valid, locale_enum = language_service.validate_locale(lang)
            if is_valid:
                return locale_enum
        
        return None


def get_request_locale(request: Request) -> LocaleEnum:
    """
    Get locale from request state.
    
    Args:
        request: FastAPI request
        
    Returns:
        Locale enum
    """
    return getattr(request.state, "locale", LocaleEnum.EN)


def get_request_cultural_context(request: Request) -> CulturalContext:
    """
    Get cultural context from request state.
    
    Args:
        request: FastAPI request
        
    Returns:
        Cultural context
    """
    return getattr(request.state, "cultural_context", CulturalContext.ENGLISH_US)


def get_language_routing_config(request: Request) -> dict:
    """
    Get language routing configuration from request state.
    
    Args:
        request: FastAPI request
        
    Returns:
        Language routing configuration dictionary
    """
    return getattr(request.state, "language_routing", {})
