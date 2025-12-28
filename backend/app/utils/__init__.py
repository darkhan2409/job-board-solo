# app/utils/__init__.py
"""
Utilities package.
"""

from app.utils.exceptions import NotFoundException, ValidationException
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_random_token,
    hash_token,
    verify_token_hash,
)
from app.utils.rate_limit import limiter
from app.utils.dependencies import (
    get_current_user,
    get_current_active_user,
    get_optional_user,
    require_role,
    oauth2_scheme,
)

__all__ = [
    # Exceptions
    "NotFoundException",
    "ValidationException",
    # Security
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "generate_random_token",
    "hash_token",
    "verify_token_hash",
    # Rate limiting
    "limiter",
    # Dependencies
    "get_current_user",
    "get_current_active_user",
    "get_optional_user",
    "require_role",
    "oauth2_scheme",
]
