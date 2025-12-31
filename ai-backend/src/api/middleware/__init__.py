"""API middleware components."""

from src.api.middleware.auth import (
    AuthenticationError,
    create_access_token,
    get_current_user,
    get_optional_user,
    get_password_hash,
    verify_password,
    verify_token,
)
from src.api.middleware.rate_limit import (
    RateLimitExceeded,
    RateLimitMiddleware,
    RateLimiter,
    rate_limiter,
)
from src.api.middleware.language import (
    LanguageDetectionMiddleware,
    get_request_locale,
    get_request_cultural_context,
    get_language_routing_config,
)

__all__ = [
    # Authentication
    "AuthenticationError",
    "create_access_token",
    "verify_token",
    "get_current_user",
    "get_optional_user",
    "verify_password",
    "get_password_hash",
    # Rate Limiting
    "RateLimitExceeded",
    "RateLimitMiddleware",
    "RateLimiter",
    "rate_limiter",
    # Language Detection
    "LanguageDetectionMiddleware",
    "get_request_locale",
    "get_request_cultural_context",
    "get_language_routing_config",
]
