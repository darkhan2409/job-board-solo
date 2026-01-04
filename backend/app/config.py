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

    # CORS Configuration
    # Comma-separated list of allowed origins
    # Development: "http://localhost:3000,https://localhost:3000"
    # Production: "https://yourdomain.com,https://www.yourdomain.com"
    # Use "*" only for public APIs (not recommended with credentials)
    CORS_ORIGINS: str = "http://localhost:3000,https://localhost:3000"
    
    # CORS settings
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_MAX_AGE: int = 3600  # Preflight cache duration in seconds

    # Application
    DEBUG: bool = True
    SECRET_KEY: str  # Required - no default for security
    API_V1_PREFIX: str = "/api"
    
    # URLs (change to https:// in production)
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"

    # API Metadata
    PROJECT_NAME: str = "Job Board API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Job board API with AI integration"

    # JWT Authentication
    JWT_SECRET_KEY: str  # Required - no default for security
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    REFRESH_TOKEN_REMEMBER_ME_EXPIRE_DAYS: int = 90

    # OAuth 2.0
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    # Supports both HTTP and HTTPS for development
    OAUTH_REDIRECT_URI: str = "http://localhost:3000/auth/callback"  # Change to https:// in production
    OAUTH_STATE_EXPIRE_MINUTES: int = 10  # OAuth state token expiration

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
    RATE_LIMIT_ENABLED: bool = False  # Temporarily disabled for debugging
    RATE_LIMIT_STORAGE_URI: str = "memory://"  # Use "redis://localhost:6379" for production
    LOGIN_RATE_LIMIT: str = "5/minute"
    REGISTER_RATE_LIMIT: str = "3/minute"
    PASSWORD_RESET_RATE_LIMIT: str = "3/hour"
    API_RATE_LIMIT: str = "100/minute"  # General API rate limit
    SEARCH_RATE_LIMIT: str = "30/minute"  # Search endpoints

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """
        Convert CORS_ORIGINS string to list and validate.
        
        Returns:
            list[str]: List of allowed origins
            
        Note:
            - Strips whitespace from each origin
            - Supports wildcard "*" for public APIs
            - Validates origin format (must start with http:// or https://)
        """
        origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        
        # Validate origins (except wildcard)
        for origin in origins:
            if origin != "*" and not (origin.startswith("http://") or origin.startswith("https://")):
                raise ValueError(f"Invalid CORS origin: {origin}. Must start with http:// or https://")
        
        return origins


# Global settings instance
settings = Settings()
