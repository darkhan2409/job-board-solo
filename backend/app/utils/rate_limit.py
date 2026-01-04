# app/utils/rate_limit.py
"""
Rate limiting configuration using SlowAPI.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings

# Initialize rate limiter
# For production, use Redis: storage_uri="redis://localhost:6379"
limiter = Limiter(
    key_func=get_remote_address,
    enabled=settings.RATE_LIMIT_ENABLED,
    storage_uri=settings.RATE_LIMIT_STORAGE_URI,
    strategy="fixed-window",
    headers_enabled=True,  # Add rate limit headers to responses
)
