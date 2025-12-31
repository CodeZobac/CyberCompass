"""
Custom exception classes for the AI Backend service.

This module defines a hierarchy of custom exceptions for different error scenarios,
providing clear error messages and recovery suggestions for users.
"""

from typing import Optional, Dict, Any
from enum import Enum


class ErrorCategory(str, Enum):
    """Categories of errors for classification and handling."""
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    RATE_LIMIT = "rate_limit"
    AI_SERVICE = "ai_service"
    MEDIA_PROCESSING = "media_processing"
    DATABASE = "database"
    WEBSOCKET = "websocket"
    CONFIGURATION = "configuration"
    EXTERNAL_SERVICE = "external_service"


class BaseAIBackendException(Exception):
    """Base exception class for all AI Backend errors."""
    
    def __init__(
        self,
        message: str,
        category: ErrorCategory,
        status_code: int = 500,
        recovery_suggestion: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.category = category
        self.status_code = status_code
        self.recovery_suggestion = recovery_suggestion or self._default_recovery_suggestion()
        self.details = details or {}
        super().__init__(self.message)
    
    def _default_recovery_suggestion(self) -> str:
        """Provide default recovery suggestion based on error category."""
        suggestions = {
            ErrorCategory.AUTHENTICATION: "Please check your authentication credentials and try again.",
            ErrorCategory.VALIDATION: "Please verify your input data and try again.",
            ErrorCategory.RATE_LIMIT: "Please wait a moment before trying again.",
            ErrorCategory.AI_SERVICE: "Our AI service is temporarily unavailable. Please try again in a few moments.",
            ErrorCategory.MEDIA_PROCESSING: "There was an issue processing your media file. Please try a different file.",
            ErrorCategory.DATABASE: "A database error occurred. Please try again later.",
            ErrorCategory.WEBSOCKET: "Connection lost. Please refresh and try again.",
            ErrorCategory.CONFIGURATION: "A configuration error occurred. Please contact support.",
            ErrorCategory.EXTERNAL_SERVICE: "An external service is unavailable. Please try again later."
        }
        return suggestions.get(self.category, "An unexpected error occurred. Please try again.")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        return {
            "error": True,
            "message": self.message,
            "category": self.category.value,
            "status_code": self.status_code,
            "recovery_suggestion": self.recovery_suggestion,
            "details": self.details
        }


# Authentication Errors
class AuthenticationError(BaseAIBackendException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            category=ErrorCategory.AUTHENTICATION,
            status_code=401,
            recovery_suggestion="Please log in again or check your authentication token.",
            details=details
        )


class InvalidTokenError(AuthenticationError):
    """Raised when JWT token is invalid or expired."""
    
    def __init__(self, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message="Invalid or expired authentication token",
            details=details
        )


class MissingAuthHeaderError(AuthenticationError):
    """Raised when authentication header is missing."""
    
    def __init__(self):
        super().__init__(
            message="Authentication header is missing",
            details={"required_header": "Authorization"}
        )


# Validation Errors
class ValidationError(BaseAIBackendException):
    """Raised when request validation fails."""
    
    def __init__(self, message: str, field_errors: Optional[Dict[str, str]] = None):
        super().__init__(
            message=message,
            category=ErrorCategory.VALIDATION,
            status_code=400,
            recovery_suggestion="Please check the highlighted fields and correct any errors.",
            details={"field_errors": field_errors or {}}
        )


class InvalidLocaleError(ValidationError):
    """Raised when an unsupported locale is provided."""
    
    def __init__(self, locale: str):
        super().__init__(
            message=f"Unsupported locale: {locale}",
            field_errors={"locale": f"Must be one of: en, pt. Got: {locale}"}
        )


class InvalidChallengeTypeError(ValidationError):
    """Raised when an invalid challenge type is requested."""
    
    def __init__(self, challenge_type: str):
        super().__init__(
            message=f"Invalid challenge type: {challenge_type}",
            field_errors={"challenge_type": f"Must be one of: deepfake_detection, social_media_sim, catfish_chat. Got: {challenge_type}"}
        )


# Rate Limiting Errors
class RateLimitError(BaseAIBackendException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, retry_after: int = 60):
        super().__init__(
            message="Rate limit exceeded",
            category=ErrorCategory.RATE_LIMIT,
            status_code=429,
            recovery_suggestion=f"Please wait {retry_after} seconds before trying again.",
            details={"retry_after": retry_after}
        )


# AI Service Errors
class AIServiceError(BaseAIBackendException):
    """Raised when AI service encounters an error."""
    
    def __init__(self, message: str = "AI service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            category=ErrorCategory.AI_SERVICE,
            status_code=503,
            recovery_suggestion="Our AI service is temporarily unavailable. We'll provide alternative content.",
            details=details
        )


class AgentUnavailableError(AIServiceError):
    """Raised when a specific agent is unavailable."""
    
    def __init__(self, agent_name: str):
        super().__init__(
            message=f"Agent '{agent_name}' is currently unavailable",
            details={"agent_name": agent_name}
        )


class CrewExecutionError(AIServiceError):
    """Raised when CrewAI execution fails."""
    
    def __init__(self, crew_name: str, error_details: str):
        super().__init__(
            message=f"Crew '{crew_name}' execution failed",
            details={"crew_name": crew_name, "error": error_details}
        )


class FlowExecutionError(AIServiceError):
    """Raised when CrewAI Flow execution fails."""
    
    def __init__(self, flow_name: str, error_details: str):
        super().__init__(
            message=f"Flow '{flow_name}' execution failed",
            details={"flow_name": flow_name, "error": error_details}
        )


class ModelInferenceError(AIServiceError):
    """Raised when LLM inference fails."""
    
    def __init__(self, model_name: str, error_details: str):
        super().__init__(
            message=f"Model '{model_name}' inference failed",
            details={"model_name": model_name, "error": error_details}
        )


# Media Processing Errors
class MediaProcessingError(BaseAIBackendException):
    """Raised when media processing fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            category=ErrorCategory.MEDIA_PROCESSING,
            status_code=422,
            recovery_suggestion="Please try uploading a different file or use a supported format.",
            details=details
        )


class UnsupportedMediaFormatError(MediaProcessingError):
    """Raised when media format is not supported."""
    
    def __init__(self, file_format: str, supported_formats: list):
        super().__init__(
            message=f"Unsupported media format: {file_format}",
            details={
                "provided_format": file_format,
                "supported_formats": supported_formats
            }
        )


class FileSizeLimitError(MediaProcessingError):
    """Raised when file size exceeds limit."""
    
    def __init__(self, file_size: int, max_size: int):
        super().__init__(
            message=f"File size ({file_size} bytes) exceeds maximum allowed size ({max_size} bytes)",
            details={
                "file_size": file_size,
                "max_size": max_size,
                "max_size_mb": max_size / (1024 * 1024)
            }
        )


# Database Errors
class DatabaseError(BaseAIBackendException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str = "Database error", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            category=ErrorCategory.DATABASE,
            status_code=500,
            recovery_suggestion="A database error occurred. Please try again in a moment.",
            details=details
        )


class ConnectionError(DatabaseError):
    """Raised when database connection fails."""
    
    def __init__(self, error_details: str):
        super().__init__(
            message="Failed to connect to database",
            details={"error": error_details}
        )


class QueryExecutionError(DatabaseError):
    """Raised when database query execution fails."""
    
    def __init__(self, query: str, error_details: str):
        super().__init__(
            message="Database query execution failed",
            details={"query": query[:100], "error": error_details}
        )


# WebSocket Errors
class WebSocketError(BaseAIBackendException):
    """Raised when WebSocket operations fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            category=ErrorCategory.WEBSOCKET,
            status_code=500,
            recovery_suggestion="Connection lost. Please refresh the page and try again.",
            details=details
        )


class WebSocketConnectionError(WebSocketError):
    """Raised when WebSocket connection fails."""
    
    def __init__(self, session_id: str, error_details: str):
        super().__init__(
            message="WebSocket connection failed",
            details={"session_id": session_id, "error": error_details}
        )


class WebSocketTimeoutError(WebSocketError):
    """Raised when WebSocket operation times out."""
    
    def __init__(self, session_id: str, timeout_seconds: int):
        super().__init__(
            message=f"WebSocket operation timed out after {timeout_seconds} seconds",
            details={"session_id": session_id, "timeout": timeout_seconds}
        )


# Configuration Errors
class ConfigurationError(BaseAIBackendException):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            category=ErrorCategory.CONFIGURATION,
            status_code=500,
            recovery_suggestion="A configuration error occurred. Please contact support.",
            details=details
        )


class MissingConfigError(ConfigurationError):
    """Raised when required configuration is missing."""
    
    def __init__(self, config_key: str):
        super().__init__(
            message=f"Missing required configuration: {config_key}",
            details={"missing_key": config_key}
        )


class InvalidConfigError(ConfigurationError):
    """Raised when configuration value is invalid."""
    
    def __init__(self, config_key: str, expected: str, actual: str):
        super().__init__(
            message=f"Invalid configuration for {config_key}",
            details={
                "config_key": config_key,
                "expected": expected,
                "actual": actual
            }
        )


# External Service Errors
class ExternalServiceError(BaseAIBackendException):
    """Raised when external service calls fail."""
    
    def __init__(self, service_name: str, error_details: str):
        super().__init__(
            message=f"External service '{service_name}' is unavailable",
            category=ErrorCategory.EXTERNAL_SERVICE,
            status_code=503,
            recovery_suggestion="An external service is temporarily unavailable. Please try again later.",
            details={"service_name": service_name, "error": error_details}
        )


class SupabaseError(ExternalServiceError):
    """Raised when Supabase operations fail."""
    
    def __init__(self, operation: str, error_details: str):
        super().__init__(
            service_name="Supabase",
            error_details=f"Operation '{operation}' failed: {error_details}"
        )
