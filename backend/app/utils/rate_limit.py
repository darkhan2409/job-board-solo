# app/utils/rate_limit.py
"""
Rate limiting configuration using SlowAPI.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    enabled=settings.RATE_LIMIT_ENABLED,
    storage_uri="memory://",  # Use in-memory storage (for production, use Redis)
    strategy="fixed-window",
)
