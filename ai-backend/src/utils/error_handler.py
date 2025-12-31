"""
Error handling and logging utilities for the AI Backend service.

This module provides centralized error handling, logging, and monitoring
integration for all components of the AI Backend.
"""

import logging
import traceback
from typing import Optional, Dict, Any, Callable
from functools import wraps
from datetime import datetime
import json

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .exceptions import (
    BaseAIBackendException,
    ErrorCategory,
    AIServiceError,
    DatabaseError,
    WebSocketError
)


# Configure structured logging
class StructuredLogger:
    """Structured logger for consistent log formatting."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create console handler with structured format
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            
            # JSON formatter for structured logs
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
                '"logger": "%(name)s", "message": "%(message)s"}'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _log_structured(self, level: str, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log with structured data."""
        log_data = {
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            **(extra or {})
        }
        
        log_method = getattr(self.logger, level.lower())
        log_method(json.dumps(log_data))
    
    def info(self, message: str, **kwargs):
        """Log info level message."""
        self._log_structured("INFO", message, kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning level message."""
        self._log_structured("WARNING", message, kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error level message."""
        self._log_structured("ERROR", message, kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical level message."""
        self._log_structured("CRITICAL", message, kwargs)
    
    def exception(self, message: str, exc: Exception, **kwargs):
        """Log exception with traceback."""
        extra = {
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "traceback": traceback.format_exc(),
            **kwargs
        }
        self._log_structured("ERROR", message, extra)


# Global logger instance
logger = StructuredLogger("ai_backend")


class ErrorMonitor:
    """Monitor and track errors for alerting and analytics."""
    
    def __init__(self):
        self.error_counts: Dict[str, int] = {}
        self.error_history: list = []
        self.max_history_size = 1000
    
    def record_error(
        self,
        error: BaseAIBackendException,
        request_id: Optional[str] = None,
        user_id: Optional[str] = None
    ):
        """Record error occurrence for monitoring."""
        error_key = f"{error.category.value}:{type(error).__name__}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        error_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "error_type": type(error).__name__,
            "category": error.category.value,
            "message": error.message,
            "status_code": error.status_code,
            "request_id": request_id,
            "user_id": user_id,
            "details": error.details
        }
        
        self.error_history.append(error_record)
        
        # Maintain history size limit
        if len(self.error_history) > self.max_history_size:
            self.error_history = self.error_history[-self.max_history_size:]
        
        # Log the error
        logger.error(
            f"Error recorded: {error.message}",
            error_type=type(error).__name__,
            category=error.category.value,
            request_id=request_id,
            user_id=user_id
        )
        
        # Check for alert conditions
        self._check_alert_conditions(error_key)
    
    def _check_alert_conditions(self, error_key: str):
        """Check if error rate exceeds alert thresholds."""
        count = self.error_counts.get(error_key, 0)
        
        # Alert if same error occurs frequently
        if count > 10:
            logger.warning(
                f"High error rate detected: {error_key}",
                error_key=error_key,
                count=count,
                alert=True
            )
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics for monitoring dashboard."""
        return {
            "total_errors": sum(self.error_counts.values()),
            "error_counts": self.error_counts,
            "recent_errors": self.error_history[-10:],
            "timestamp": datetime.utcnow().isoformat()
        }


# Global error monitor instance
error_monitor = ErrorMonitor()


def handle_exception(
    exc: Exception,
    request_id: Optional[str] = None,
    user_id: Optional[str] = None
) -> JSONResponse:
    """
    Handle exceptions and convert to appropriate HTTP responses.
    
    Args:
        exc: The exception to handle
        request_id: Optional request ID for tracking
        user_id: Optional user ID for tracking
    
    Returns:
        JSONResponse with error details
    """
    # Handle custom exceptions
    if isinstance(exc, BaseAIBackendException):
        error_monitor.record_error(exc, request_id, user_id)
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict()
        )
    
    # Handle validation errors
    if isinstance(exc, RequestValidationError):
        logger.error(
            "Validation error",
            errors=str(exc.errors()),
            request_id=request_id
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": True,
                "message": "Validation error",
                "category": ErrorCategory.VALIDATION.value,
                "details": {"validation_errors": exc.errors()},
                "recovery_suggestion": "Please check your input data and try again."
            }
        )
    
    # Handle HTTP exceptions
    if isinstance(exc, StarletteHTTPException):
        logger.error(
            "HTTP exception",
            status_code=exc.status_code,
            detail=exc.detail,
            request_id=request_id
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "category": "http_error",
                "recovery_suggestion": "Please try again or contact support if the issue persists."
            }
        )
    
    # Handle unexpected exceptions
    logger.exception("Unexpected error", exc=exc, request_id=request_id)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "An unexpected error occurred",
            "category": "internal_error",
            "recovery_suggestion": "Please try again later or contact support if the issue persists.",
            "details": {"error_type": type(exc).__name__}
        }
    )


def error_handler_middleware(app):
    """
    Middleware to catch and handle all exceptions.
    
    Usage:
        app = FastAPI()
        error_handler_middleware(app)
    """
    
    @app.exception_handler(BaseAIBackendException)
    async def custom_exception_handler(request: Request, exc: BaseAIBackendException):
        request_id = request.headers.get("X-Request-ID")
        user_id = request.state.user_id if hasattr(request.state, "user_id") else None
        return handle_exception(exc, request_id, user_id)
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        request_id = request.headers.get("X-Request-ID")
        return handle_exception(exc, request_id)
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        request_id = request.headers.get("X-Request-ID")
        return handle_exception(exc, request_id)
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        request_id = request.headers.get("X-Request-ID")
        user_id = request.state.user_id if hasattr(request.state, "user_id") else None
        return handle_exception(exc, request_id, user_id)


def with_error_handling(func: Callable):
    """
    Decorator to add error handling to async functions.
    
    Usage:
        @with_error_handling
        async def my_function():
            # function code
    """
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except BaseAIBackendException:
            # Re-raise custom exceptions
            raise
        except Exception as e:
            # Convert unexpected exceptions to AIServiceError
            logger.exception(f"Error in {func.__name__}", exc=e)
            raise AIServiceError(
                message=f"Error executing {func.__name__}",
                details={"function": func.__name__, "error": str(e)}
            )
    
    return wrapper


def with_retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry failed operations.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds
    
    Usage:
        @with_retry(max_attempts=3, delay=2.0)
        async def my_function():
            # function code
    """
    
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            import asyncio
            
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except (DatabaseError, ExternalServiceError) as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Retry attempt {attempt + 1}/{max_attempts} for {func.__name__}",
                            error=str(e)
                        )
                        await asyncio.sleep(delay * (attempt + 1))
                    else:
                        logger.error(
                            f"All retry attempts failed for {func.__name__}",
                            attempts=max_attempts,
                            error=str(e)
                        )
                except BaseAIBackendException:
                    # Don't retry other custom exceptions
                    raise
            
            # Raise the last exception if all retries failed
            if last_exception:
                raise last_exception
        
        return wrapper
    
    return decorator


class ErrorContext:
    """Context manager for error handling with automatic logging."""
    
    def __init__(self, operation: str, **context):
        self.operation = operation
        self.context = context
    
    async def __aenter__(self):
        logger.info(f"Starting operation: {self.operation}", **self.context)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.exception(
                f"Error in operation: {self.operation}",
                exc=exc_val,
                **self.context
            )
            
            # Convert to appropriate exception if needed
            if not isinstance(exc_val, BaseAIBackendException):
                # Let the exception propagate for middleware to handle
                return False
        else:
            logger.info(f"Completed operation: {self.operation}", **self.context)
        
        return False  # Don't suppress exceptions


# Health check utilities
class HealthChecker:
    """Monitor service health and component status."""
    
    def __init__(self):
        self.component_status: Dict[str, bool] = {}
        self.last_check: Dict[str, datetime] = {}
    
    async def check_component(self, component_name: str, check_func: Callable) -> bool:
        """
        Check health of a specific component.
        
        Args:
            component_name: Name of the component to check
            check_func: Async function that returns True if healthy
        
        Returns:
            True if component is healthy, False otherwise
        """
        try:
            is_healthy = await check_func()
            self.component_status[component_name] = is_healthy
            self.last_check[component_name] = datetime.utcnow()
            
            if not is_healthy:
                logger.warning(f"Component unhealthy: {component_name}")
            
            return is_healthy
        except Exception as e:
            logger.exception(f"Health check failed for {component_name}", exc=e)
            self.component_status[component_name] = False
            self.last_check[component_name] = datetime.utcnow()
            return False
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status."""
        all_healthy = all(self.component_status.values()) if self.component_status else False
        
        return {
            "healthy": all_healthy,
            "components": {
                name: {
                    "healthy": status,
                    "last_check": self.last_check.get(name, datetime.utcnow()).isoformat()
                }
                for name, status in self.component_status.items()
            },
            "timestamp": datetime.utcnow().isoformat()
        }


# Global health checker instance
health_checker = HealthChecker()
