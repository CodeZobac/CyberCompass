"""Pydantic models for API responses."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Error detail structure."""

    field: Optional[str] = Field(default=None, description="Field that caused the error")
    message: str = Field(..., description="Error message")
    code: Optional[str] = Field(default=None, description="Error code")


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Error detail message")
    errors: Optional[List[ErrorDetail]] = Field(
        default=None, description="Field-level errors"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")
    path: Optional[str] = Field(default=None, description="Request path")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "detail": "Request validation failed",
                "errors": [
                    {"field": "email", "message": "Invalid email format", "code": "invalid_email"}
                ],
                "timestamp": "2024-01-15T10:30:00Z",
                "path": "/api/v1/auth/login",
            }
        }


class SuccessResponse(BaseModel):
    """Standard success response."""

    success: bool = Field(default=True, description="Success status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""

    items: List[Any] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")
    dependencies: Optional[Dict[str, str]] = Field(
        default=None, description="Dependency health status"
    )
