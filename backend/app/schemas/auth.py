# app/schemas/auth.py
"""
Pydantic schemas for authentication-related requests and responses.
"""

from pydantic import BaseModel

from app.schemas.user import UserResponse


class TokenResponse(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""

    refresh_token: str


class OAuthCallbackRequest(BaseModel):
    """Schema for OAuth callback request."""

    code: str
    state: str


class OAuthUrlResponse(BaseModel):
    """Schema for OAuth authorization URL response."""

    authorization_url: str
