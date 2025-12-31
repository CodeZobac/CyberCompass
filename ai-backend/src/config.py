"""Application configuration management."""

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="Cyber Compass AI Backend")
    app_version: str = Field(default="2.0.0")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    workers: int = Field(default=4)

    # Security
    secret_key: str = Field(default="change-me-in-production")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expiration_minutes: int = Field(default=60)
    cors_origins: str = Field(default="http://localhost:3000")

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/cyber_compass_ai"
    )
    database_pool_size: int = Field(default=20)
    database_max_overflow: int = Field(default=10)

    # Supabase
    supabase_url: str = Field(default="")
    supabase_key: str = Field(default="")
    supabase_service_role_key: str = Field(default="")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")
    redis_max_connections: int = Field(default=50)

    # OpenAI
    openai_api_key: str = Field(default="")
    openai_model: str = Field(default="gpt-4")
    openai_temperature: float = Field(default=0.7)

    # CrewAI
    crewai_verbose: bool = Field(default=True)
    crewai_memory_enabled: bool = Field(default=True)
    crewai_max_iterations: int = Field(default=10)

    # File Storage
    upload_dir: str = Field(default="./uploads")
    max_upload_size_mb: int = Field(default=50)

    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60)
    rate_limit_burst: int = Field(default=10)

    # WebSocket
    websocket_ping_interval: int = Field(default=30)
    websocket_ping_timeout: int = Field(default=10)
    max_websocket_connections: int = Field(default=1000)

    # Analytics
    analytics_batch_size: int = Field(default=100)
    analytics_flush_interval: int = Field(default=300)

    # Localization
    default_locale: str = Field(default="en")
    supported_locales: str = Field(default="en,pt")

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def supported_locales_list(self) -> List[str]:
        """Parse supported locales from comma-separated string."""
        return [locale.strip() for locale in self.supported_locales.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
