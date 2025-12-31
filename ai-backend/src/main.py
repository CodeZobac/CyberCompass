"""FastAPI application entry point with lifespan management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.middleware import RateLimitMiddleware, LanguageDetectionMiddleware
from src.api.routes import (
    auth_router,
    conversations_router,
    websocket_router,
    analytics_router,
    cultural_content_router,
)
from src.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifespan - startup and shutdown events."""
    # Startup
    print("🚀 Initializing Cyber Compass AI Backend...")
    print(f"📦 Version: {settings.app_version}")
    print(f"🌍 Environment: {settings.environment}")
    print("🤖 CrewAI agents will be initialized in task 2...")
    print("✅ AI Backend ready!")

    yield

    # Shutdown
    print("🔄 Shutting down AI Backend...")
    print("✅ Cleanup complete!")


app = FastAPI(
    title=settings.app_name,
    description="CrewAI-powered backend for cyber ethics education",
    version=settings.app_version,
    lifespan=lifespan,
    debug=settings.debug,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Add language detection middleware
app.add_middleware(LanguageDetectionMiddleware)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(conversations_router, prefix="/api/v1")
app.include_router(websocket_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(cultural_content_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint - health check."""
    return {
        "message": "Cyber Compass AI Backend",
        "version": settings.app_version,
        "status": "operational",
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "ai-backend"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
