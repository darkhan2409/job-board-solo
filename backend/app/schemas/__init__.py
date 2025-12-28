# app/schemas/__init__.py
"""
Pydantic schemas package for request/response validation.
"""

from app.schemas.company import (
    CompanyBase,
    CompanyCreate,
    CompanyResponse,
    CompanyWithJobs
)
from app.schemas.job import (
    JobBase,
    JobCreate,
    JobUpdate,
    JobResponse,
    JobFilters
)
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    PasswordChange,
    EmailVerification,
    PasswordResetRequest,
    PasswordReset,
)
from app.schemas.auth import (
    TokenResponse,
    RefreshTokenRequest,
    OAuthCallbackRequest,
    OAuthUrlResponse,
)
from app.schemas.saved_job import (
    SavedJobResponse,
    SavedJobCreate,
)
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationWithoutJob,
)

__all__ = [
    # Company schemas
    "CompanyBase",
    "CompanyCreate",
    "CompanyResponse",
    "CompanyWithJobs",
    # Job schemas
    "JobBase",
    "JobCreate",
    "JobUpdate",
    "JobResponse",
    "JobFilters",
    # User schemas
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "PasswordChange",
    "EmailVerification",
    "PasswordResetRequest",
    "PasswordReset",
    # Auth schemas
    "TokenResponse",
    "RefreshTokenRequest",
    "OAuthCallbackRequest",
    "OAuthUrlResponse",
    # Saved job schemas
    "SavedJobResponse",
    "SavedJobCreate",
    # Application schemas
    "ApplicationCreate",
    "ApplicationUpdate",
    "ApplicationResponse",
    "ApplicationWithoutJob",
]
