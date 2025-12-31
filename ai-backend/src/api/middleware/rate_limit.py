"""Rate limiting middleware to prevent API abuse."""

import time
from collections import defaultdict
from typing import Callable, Dict, Tuple

from fastapi import HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import get_settings

settings = get_settings()


class RateLimitExceeded(HTTPException):
    """Rate limit exceeded error."""

    def __init__(self, retry_after: int):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)},
        )


class RateLimiter:
    """
    Token bucket rate limiter implementation.

    Uses a sliding window approach to track requests per client.
    """

    def __init__(
        self,
        rate_limit_per_minute: int = settings.rate_limit_per_minute,
        burst: int = settings.rate_limit_burst,
    ):
        """
        Initialize rate limiter.

        Args:
            rate_limit_per_minute: Maximum requests allowed per minute
            burst: Maximum burst size (tokens in bucket)
        """
        self.rate_limit = rate_limit_per_minute
        self.burst = burst
        self.window_size = 60  # 1 minute in seconds

        # Storage: {client_id: (tokens, last_update_time)}
        self.clients: Dict[str, Tuple[float, float]] = defaultdict(
            lambda: (float(burst), time.time())
        )

    def _get_client_id(self, request: Request) -> str:
        """
        Get unique client identifier from request.

        Uses user_id from auth if available, otherwise falls back to IP.

        Args:
            request: FastAPI request object

        Returns:
            Client identifier string
        """
        # Try to get user_id from request state (set by auth middleware)
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"

        # Fall back to IP address
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return f"ip:{forwarded.split(',')[0].strip()}"

        client_host = request.client.host if request.client else "unknown"
        return f"ip:{client_host}"

    def _refill_tokens(self, tokens: float, last_update: float) -> Tuple[float, float]:
        """
        Refill tokens based on elapsed time.

        Args:
            tokens: Current token count
            last_update: Last update timestamp

        Returns:
            Tuple of (new_token_count, current_time)
        """
        now = time.time()
        elapsed = now - last_update

        # Calculate tokens to add based on rate limit
        tokens_to_add = (elapsed / self.window_size) * self.rate_limit
        new_tokens = min(self.burst, tokens + tokens_to_add)

        return new_tokens, now

    def check_rate_limit(self, request: Request) -> None:
        """
        Check if request is within rate limit.

        Args:
            request: FastAPI request object

        Raises:
            RateLimitExceeded: If rate limit is exceeded
        """
        client_id = self._get_client_id(request)

        # Get current state
        tokens, last_update = self.clients[client_id]

        # Refill tokens
        tokens, now = self._refill_tokens(tokens, last_update)

        # Check if we have tokens available
        if tokens < 1:
            # Calculate retry after time
            tokens_needed = 1 - tokens
            retry_after = int((tokens_needed / self.rate_limit) * self.window_size) + 1
            raise RateLimitExceeded(retry_after=retry_after)

        # Consume one token
        tokens -= 1
        self.clients[client_id] = (tokens, now)

    def cleanup_old_clients(self, max_age: int = 3600) -> None:
        """
        Remove old client entries to prevent memory leaks.

        Args:
            max_age: Maximum age in seconds before cleanup
        """
        now = time.time()
        to_remove = [
            client_id
            for client_id, (_, last_update) in self.clients.items()
            if now - last_update > max_age
        ]

        for client_id in to_remove:
            del self.clients[client_id]


# Global rate limiter instance
rate_limiter = RateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for rate limiting."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request with rate limiting.

        Args:
            request: FastAPI request
            call_next: Next middleware/handler

        Returns:
            Response from handler

        Raises:
            RateLimitExceeded: If rate limit is exceeded
        """
        # Skip rate limiting for health check endpoints
        if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Check rate limit
        try:
            rate_limiter.check_rate_limit(request)
        except RateLimitExceeded as e:
            # Periodically cleanup old clients
            if time.time() % 300 < 1:  # Every ~5 minutes
                rate_limiter.cleanup_old_clients()
            raise e

        # Process request
        response = await call_next(request)

        # Add rate limit headers
        client_id = rate_limiter._get_client_id(request)
        tokens, _ = rate_limiter.clients.get(
            client_id, (float(rate_limiter.burst), time.time())
        )

        response.headers["X-RateLimit-Limit"] = str(rate_limiter.rate_limit)
        response.headers["X-RateLimit-Remaining"] = str(int(tokens))
        response.headers["X-RateLimit-Reset"] = str(int(time.time() + 60))

        return response
