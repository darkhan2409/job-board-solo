# app/routes/auth.py
"""
Authentication and user management routes.
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import (
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
from app.services import auth_service, user_service, oauth_service
from app.utils.dependencies import get_current_active_user
from app.utils.exceptions import ValidationException, NotFoundException
from app.utils.rate_limit import limiter
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account and send verification email",
)
@limiter.limit(settings.REGISTER_RATE_LIMIT)
async def register(
    request: Request,
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Register a new user.

    - Validates password strength
    - Creates user account
    - Sends verification email
    - Returns user data (unverified)
    """
    try:
        user = await auth_service.register_user(
            db=db,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
            role=user_data.role,
        )
        return user
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/verify-email",
    response_model=UserResponse,
    summary="Verify email address",
    description="Verify user's email using verification token",
)
async def verify_email(
    verification_data: EmailVerification,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Verify user's email address.

    - Validates verification token
    - Marks user as verified
    - Sends welcome email
    """
    try:
        user = await auth_service.verify_email(
            db=db,
            token=verification_data.token,
        )
        return user
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.post(
    "/resend-verification",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Resend verification email",
    description="Resend verification email to user",
)
@limiter.limit("3/hour")
async def resend_verification(
    request: Request,
    email_data: PasswordResetRequest,  # Reusing this schema as it only has email field
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Resend verification email to user.

    - Generates new verification token
    - Sends verification email
    - Rate limited to 3 requests per hour
    """
    try:
        await auth_service.resend_verification_email(
            db=db,
            email=email_data.email,
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description="Authenticate user and generate JWT tokens",
)
@limiter.limit(settings.LOGIN_RATE_LIMIT)
async def login(
    request: Request,
    login_data: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Authenticate user and return JWT tokens.

    - Validates credentials
    - Checks if email is verified
    - Generates access and refresh tokens
    - Supports "remember me" option (90 days refresh token)
    """
    try:
        access_token, refresh_token, user = await auth_service.login(
            db=db,
            email=login_data.email,
            password=login_data.password,
            remember_me=login_data.remember_me,
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.model_validate(user),
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Generate new access token using refresh token (with rotation)",
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Refresh access token using refresh token.

    - Validates refresh token
    - Generates new access and refresh tokens (rotation)
    - Revokes old refresh token
    """
    try:
        new_access_token, new_refresh_token = await auth_service.refresh_access_token(
            db=db,
            refresh_token_str=refresh_data.refresh_token,
        )

        # Get user from new access token
        from app.utils.security import decode_token
        payload = decode_token(new_access_token)
        user_id = int(payload.get("sub"))

        user = await user_service.get_user_by_id(db=db, user_id=user_id)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            user=UserResponse.model_validate(user),
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout user",
    description="Revoke refresh token (logout)",
)
async def logout(
    refresh_data: RefreshTokenRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Logout user by revoking refresh token.

    - Revokes refresh token
    - Client should delete both access and refresh tokens
    """
    try:
        await auth_service.logout(
            db=db,
            refresh_token_str=refresh_data.refresh_token,
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/request-password-reset",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Request password reset",
    description="Send password reset email to user",
)
@limiter.limit("3/minute")
async def request_password_reset(
    request: Request,
    reset_request: PasswordResetRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Request password reset.

    - Generates password reset token
    - Sends password reset email
    - Always returns 204 (security: don't reveal if email exists)
    """
    await auth_service.request_password_reset(
        db=db,
        email=reset_request.email,
    )


@router.post(
    "/reset-password",
    response_model=UserResponse,
    summary="Reset password",
    description="Reset user's password using reset token",
)
async def reset_password(
    reset_data: PasswordReset,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Reset user's password.

    - Validates reset token
    - Updates password
    - Revokes all refresh tokens (force re-login)
    """
    try:
        user = await auth_service.reset_password(
            db=db,
            token=reset_data.token,
            new_password=reset_data.new_password,
        )
        return user
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/google",
    response_model=OAuthUrlResponse,
    summary="Get Google OAuth URL",
    description="Generate Google OAuth authorization URL",
)
async def google_auth_url(db: Annotated[AsyncSession, Depends(get_db)]):
    """
    Get Google OAuth authorization URL.

    - Generates state parameter for CSRF protection
    - Stores state in database with expiration
    - Returns authorization URL for client redirect
    """
    try:
        # Create and store state token
        state = await oauth_service.create_oauth_state(db=db, provider='google')
        
        # Generate OAuth URL with state
        auth_url = oauth_service.get_google_auth_url(state=state)
        return OAuthUrlResponse(authorization_url=auth_url)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/google/callback",
    response_model=TokenResponse,
    summary="Google OAuth callback",
    description="Handle Google OAuth callback and login user",
)
async def google_callback(
    callback_data: OAuthCallbackRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Handle Google OAuth callback.

    - Validates state parameter for CSRF protection
    - Exchanges authorization code for access token
    - Gets user info from Google
    - Creates or updates user account
    - Returns JWT tokens
    """
    try:
        access_token, refresh_token, user = await oauth_service.handle_google_callback(
            db=db,
            code=callback_data.code,
            state=callback_data.state,
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.model_validate(user),
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/github",
    response_model=OAuthUrlResponse,
    summary="Get GitHub OAuth URL",
    description="Generate GitHub OAuth authorization URL",
)
async def github_auth_url(db: Annotated[AsyncSession, Depends(get_db)]):
    """
    Get GitHub OAuth authorization URL.

    - Generates state parameter for CSRF protection
    - Stores state in database with expiration
    - Returns authorization URL for client redirect
    """
    try:
        # Create and store state token
        state = await oauth_service.create_oauth_state(db=db, provider='github')
        
        # Generate OAuth URL with state
        auth_url = oauth_service.get_github_auth_url(state=state)
        return OAuthUrlResponse(authorization_url=auth_url)
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/github/callback",
    response_model=TokenResponse,
    summary="GitHub OAuth callback",
    description="Handle GitHub OAuth callback and login user",
)
async def github_callback(
    callback_data: OAuthCallbackRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Handle GitHub OAuth callback.

    - Validates state parameter for CSRF protection
    - Exchanges authorization code for access token
    - Gets user info from GitHub
    - Creates or updates user account
    - Returns JWT tokens
    """
    try:
        access_token, refresh_token, user = await oauth_service.handle_github_callback(
            db=db,
            code=callback_data.code,
            state=callback_data.state,
        )
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.model_validate(user),
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get current authenticated user's profile",
)
async def get_current_user_profile(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
):
    """
    Get current authenticated user's profile.

    Requires valid JWT access token.
    """
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update user profile",
    description="Update current user's profile information",
)
async def update_profile(
    update_data: UserUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Update current user's profile.

    - Can update full name and email
    - Email change requires re-verification
    """
    try:
        # Get full user object from DB
        user = await user_service.get_user_by_id(db=db, user_id=current_user.id)

        updated_user = await user_service.update_user_profile(
            db=db,
            user=user,
            full_name=update_data.full_name,
            email=update_data.email,
        )
        return updated_user
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/change-password",
    response_model=UserResponse,
    summary="Change password",
    description="Change current user's password",
)
async def change_password_endpoint(
    password_data: PasswordChange,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Change current user's password.

    - Requires current password for verification
    - Validates new password strength
    """
    try:
        # Get full user object from DB
        user = await user_service.get_user_by_id(db=db, user_id=current_user.id)

        updated_user = await user_service.change_password(
            db=db,
            user=user,
            current_password=password_data.current_password,
            new_password=password_data.new_password,
        )
        return updated_user
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
