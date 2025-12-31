"""API route handlers."""

from src.api.routes.auth import router as auth_router
from src.api.routes.conversations import router as conversations_router
from src.api.routes.websocket import router as websocket_router
from src.api.routes.analytics import router as analytics_router
from src.api.routes.cultural_content import router as cultural_content_router

__all__ = [
    "auth_router",
    "conversations_router",
    "websocket_router",
    "analytics_router",
    "cultural_content_router",
]
