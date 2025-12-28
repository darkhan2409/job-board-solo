# app/config.py
"""
Application configuration using Pydantic Settings.
Loads environment variables from .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./jobs.db"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # Application
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    API_V1_PREFIX: str = "/api"

    # API Metadata
    PROJECT_NAME: str = "Job Board API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Job board API with AI integration"

    # JWT Authentication
    JWT_SECRET_KEY: str = "your-jwt-secret-key-please-change-in-production-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    REFRESH_TOKEN_REMEMBER_ME_EXPIRE_DAYS: int = 90

    # OAuth 2.0
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    OAUTH_REDIRECT_URI: str = "http://localhost:3000/auth/callback"

    # Email / SMTP
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    SMTP_FROM_NAME: str = "Job Board"
    EMAIL_VERIFICATION_EXPIRE_HOURS: int = 24
    PASSWORD_RESET_EXPIRE_HOURS: int = 1

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    LOGIN_RATE_LIMIT: str = "5/minute"
    REGISTER_RATE_LIMIT: str = "3/minute"
    PASSWORD_RESET_RATE_LIMIT: str = "3/hour"

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Convert CORS_ORIGINS string to list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
