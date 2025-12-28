# app/services/__init__.py
"""
Business logic services package.
"""

from app.services.job_service import JobService
from app.services.company_service import CompanyService
from app.services.saved_job_service import SavedJobService
from app.services.application_service import ApplicationService

from app.services.email_service import (
    send_email,
    send_verification_email,
    send_password_reset_email,
    send_welcome_email,
)

from app.services.auth_service import (
    register_user,
    verify_email,
    login,
    refresh_access_token,
    logout,
    request_password_reset,
    reset_password,
)

from app.services.user_service import (
    get_user_by_id,
    get_user_by_email,
    update_user_profile,
    change_password,
    deactivate_user,
    reactivate_user,
)

from app.services.oauth_service import (
    get_google_auth_url,
    get_github_auth_url,
    handle_google_callback,
    handle_github_callback,
)

__all__ = [
    # Existing services
    "JobService",
    "CompanyService",
    "SavedJobService",
    "ApplicationService",
    # Email service
    "send_email",
    "send_verification_email",
    "send_password_reset_email",
    "send_welcome_email",
    # Auth service
    "register_user",
    "verify_email",
    "login",
    "refresh_access_token",
    "logout",
    "request_password_reset",
    "reset_password",
    # User service
    "get_user_by_id",
    "get_user_by_email",
    "update_user_profile",
    "change_password",
    "deactivate_user",
    "reactivate_user",
    # OAuth service
    "get_google_auth_url",
    "get_github_auth_url",
    "handle_google_callback",
    "handle_github_callback",
]
