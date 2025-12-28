# app/schemas/user.py
"""
Pydantic schemas for user-related requests and responses.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=8, max_length=100)
    role: Optional[UserRole] = UserRole.REGULAR_USER

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str
    remember_me: bool = False


class UserResponse(UserBase):
    """Schema for user response (public data)."""

    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    oauth_provider: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class PasswordChange(BaseModel):
    """Schema for changing password."""

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class EmailVerification(BaseModel):
    """Schema for email verification."""

    token: str


class PasswordResetRequest(BaseModel):
    """Schema for requesting password reset."""

    email: EmailStr


class PasswordReset(BaseModel):
    """Schema for resetting password."""

    token: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v
