# app/utils/security.py
"""
Security utilities for password hashing and JWT token management.
"""

import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary of claims to encode in the token
        expires_delta: Optional custom expiration time delta

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(data: Dict[str, Any], remember_me: bool = False) -> str:
    """
    Create a JWT refresh token.

    Args:
        data: Dictionary of claims to encode in the token
        remember_me: If True, token expires in 90 days instead of 30

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if remember_me:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_REMEMBER_ME_EXPIRE_DAYS)
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token string to decode

    Returns:
        Dictionary of claims if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def generate_random_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token.

    Used for email verification and password reset tokens.

    Args:
        length: Length of the token in bytes (default: 32)

    Returns:
        Hex-encoded random token string
    """
    return secrets.token_urlsafe(length)


def hash_token(token: str) -> str:
    """
    Hash a token for secure storage.

    Used for refresh tokens to prevent them from being reused if stolen.

    Args:
        token: Token string to hash

    Returns:
        Hashed token string
    """
    return pwd_context.hash(token)


def verify_token_hash(token: str, hashed_token: str) -> bool:
    """
    Verify a token against its hash.

    Args:
        token: Plain token string
        hashed_token: Hashed token to compare against

    Returns:
        True if token matches hash, False otherwise
    """
    return pwd_context.verify(token, hashed_token)
