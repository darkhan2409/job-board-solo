# app/services/oauth_service.py
"""
OAuth service for Google and GitHub authentication.
"""

import logging
from typing import Dict, Optional, Tuple
from urllib.parse import urlencode

import httpx
from authlib.integrations.httpx_client import AsyncOAuth2Client
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User, UserRole
from app.models.refresh_token import RefreshToken
from app.models.oauth_state import OAuthState
from app.utils.security import create_access_token, create_refresh_token, hash_token, generate_random_token
from app.utils.exceptions import ValidationException
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# OAuth provider configurations
GOOGLE_CONFIG = {
    "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
    "token_url": "https://oauth2.googleapis.com/token",
    "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo",
    "scopes": ["openid", "email", "profile"],
}

GITHUB_CONFIG = {
    "authorize_url": "https://github.com/login/oauth/authorize",
    "token_url": "https://github.com/login/oauth/access_token",
    "userinfo_url": "https://api.github.com/user",
    "scopes": ["user:email"],
}


async def create_oauth_state(db: AsyncSession, provider: str) -> str:
    """
    Create and store OAuth state token for CSRF protection.

    Args:
        db: Database session
        provider: OAuth provider ('google' or 'github')

    Returns:
        State token string

    Raises:
        ValidationException: If provider is invalid
    """
    if provider not in ['google', 'github']:
        raise ValidationException(f"Invalid OAuth provider: {provider}")

    # Generate random state token
    state = generate_random_token()
    expires_at = datetime.utcnow() + timedelta(minutes=settings.OAUTH_STATE_EXPIRE_MINUTES)

    # Store in database
    oauth_state = OAuthState(
        state=state,
        provider=provider,
        expires_at=expires_at,
    )

    db.add(oauth_state)
    await db.commit()

    logger.info(f"Created OAuth state token for {provider}")

    return state


async def validate_oauth_state(db: AsyncSession, state: str, provider: str) -> None:
    """
    Validate OAuth state token for CSRF protection.

    Args:
        db: Database session
        state: State token from OAuth callback
        provider: OAuth provider ('google' or 'github')

    Raises:
        ValidationException: If state is invalid, expired, or already used
    """
    if not state:
        raise ValidationException("Missing state parameter")

    # Find state token
    stmt = select(OAuthState).where(
        OAuthState.state == state,
        OAuthState.provider == provider,
    )
    result = await db.execute(stmt)
    oauth_state = result.scalar_one_or_none()

    if not oauth_state:
        raise ValidationException("Invalid state parameter - possible CSRF attack")

    if oauth_state.used:
        raise ValidationException("State token already used - possible replay attack")

    if oauth_state.expires_at < datetime.utcnow():
        raise ValidationException("State token expired")

    # Mark as used
    oauth_state.used = True
    await db.commit()

    logger.info(f"Validated OAuth state token for {provider}")


def get_google_auth_url(state: str) -> str:
    """
    Generate Google OAuth authorization URL.

    Args:
        state: Random state parameter for CSRF protection

    Returns:
        Authorization URL
    """
    if not settings.GOOGLE_CLIENT_ID:
        raise ValidationException("Google OAuth not configured")

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.OAUTH_REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(GOOGLE_CONFIG["scopes"]),
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }

    return f"{GOOGLE_CONFIG['authorize_url']}?{urlencode(params)}"


def get_github_auth_url(state: str) -> str:
    """
    Generate GitHub OAuth authorization URL.

    Args:
        state: Random state parameter for CSRF protection

    Returns:
        Authorization URL
    """
    if not settings.GITHUB_CLIENT_ID:
        raise ValidationException("GitHub OAuth not configured")

    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": settings.OAUTH_REDIRECT_URI,
        "scope": " ".join(GITHUB_CONFIG["scopes"]),
        "state": state,
    }

    return f"{GITHUB_CONFIG['authorize_url']}?{urlencode(params)}"


async def handle_google_callback(
    db: AsyncSession,
    code: str,
    state: str,
) -> Tuple[str, str, User]:
    """
    Handle Google OAuth callback and create/login user.

    Args:
        db: Database session
        code: Authorization code from Google
        state: State parameter for CSRF validation

    Returns:
        Tuple of (access_token, refresh_token, user)

    Raises:
        ValidationException: If OAuth flow fails or state validation fails
    """
    # Validate state token for CSRF protection
    await validate_oauth_state(db=db, state=state, provider='google')

    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise ValidationException("Google OAuth not configured")

    try:
        # Exchange code for access token
        async with httpx.AsyncClient() as client:
            oauth_client = AsyncOAuth2Client(
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                redirect_uri=settings.OAUTH_REDIRECT_URI,
            )

            token_response = await oauth_client.fetch_token(
                url=GOOGLE_CONFIG["token_url"],
                code=code,
                grant_type="authorization_code",
            )

            # Get user info
            access_token = token_response.get("access_token")
            headers = {"Authorization": f"Bearer {access_token}"}

            userinfo_response = await client.get(
                GOOGLE_CONFIG["userinfo_url"],
                headers=headers,
            )
            userinfo_response.raise_for_status()
            userinfo = userinfo_response.json()

    except Exception as e:
        logger.error(f"Google OAuth error: {e}")
        raise ValidationException("Google authentication failed")

    # Extract user data
    email = userinfo.get("email")
    full_name = userinfo.get("name", email)
    google_id = userinfo.get("id")

    if not email or not google_id:
        raise ValidationException("Failed to get user info from Google")

    # Find or create user
    user = await _find_or_create_oauth_user(
        db=db,
        email=email,
        full_name=full_name,
        provider="google",
        provider_id=google_id,
    )

    # Generate JWT tokens
    access_token, refresh_token = await _generate_tokens_for_user(db, user)

    logger.info(f"User {user.email} logged in via Google")

    return access_token, refresh_token, user


async def handle_github_callback(
    db: AsyncSession,
    code: str,
    state: str,
) -> Tuple[str, str, User]:
    """
    Handle GitHub OAuth callback and create/login user.

    Args:
        db: Database session
        code: Authorization code from GitHub
        state: State parameter for CSRF validation

    Returns:
        Tuple of (access_token, refresh_token, user)

    Raises:
        ValidationException: If OAuth flow fails or state validation fails
    """
    # Validate state token for CSRF protection
    await validate_oauth_state(db=db, state=state, provider='github')

    if not settings.GITHUB_CLIENT_ID or not settings.GITHUB_CLIENT_SECRET:
        raise ValidationException("GitHub OAuth not configured")

    try:
        # Exchange code for access token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GITHUB_CONFIG["token_url"],
                data={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": settings.OAUTH_REDIRECT_URI,
                },
                headers={"Accept": "application/json"},
            )
            token_response.raise_for_status()
            token_data = token_response.json()

            access_token = token_data.get("access_token")
            if not access_token:
                raise ValidationException("Failed to get access token from GitHub")

            # Get user info
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }

            userinfo_response = await client.get(
                GITHUB_CONFIG["userinfo_url"],
                headers=headers,
            )
            userinfo_response.raise_for_status()
            userinfo = userinfo_response.json()

            # Get primary email (GitHub may not return email in profile)
            email = userinfo.get("email")
            if not email:
                emails_response = await client.get(
                    "https://api.github.com/user/emails",
                    headers=headers,
                )
                emails_response.raise_for_status()
                emails = emails_response.json()

                # Find primary verified email
                for email_obj in emails:
                    if email_obj.get("primary") and email_obj.get("verified"):
                        email = email_obj.get("email")
                        break

    except Exception as e:
        logger.error(f"GitHub OAuth error: {e}")
        raise ValidationException("GitHub authentication failed")

    # Extract user data
    full_name = userinfo.get("name") or userinfo.get("login", email)
    github_id = str(userinfo.get("id"))

    if not email or not github_id:
        raise ValidationException("Failed to get user info from GitHub")

    # Find or create user
    user = await _find_or_create_oauth_user(
        db=db,
        email=email,
        full_name=full_name,
        provider="github",
        provider_id=github_id,
    )

    # Generate JWT tokens
    access_token, refresh_token = await _generate_tokens_for_user(db, user)

    logger.info(f"User {user.email} logged in via GitHub")

    return access_token, refresh_token, user


async def _find_or_create_oauth_user(
    db: AsyncSession,
    email: str,
    full_name: str,
    provider: str,
    provider_id: str,
) -> User:
    """
    Find existing OAuth user or create new one.

    Args:
        db: Database session
        email: User's email
        full_name: User's full name
        provider: OAuth provider (google/github)
        provider_id: Provider-specific user ID

    Returns:
        User instance
    """
    # Try to find by OAuth provider ID
    stmt = select(User).where(
        User.oauth_provider == provider,
        User.oauth_provider_id == provider_id,
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        return user

    # Try to find by email
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        # Link OAuth account to existing user
        user.oauth_provider = provider
        user.oauth_provider_id = provider_id
        user.is_verified = True  # OAuth users are pre-verified

        await db.commit()
        await db.refresh(user)

        logger.info(f"Linked {provider} account to existing user {user.email}")
        return user

    # Create new user
    user = User(
        email=email,
        full_name=full_name,
        oauth_provider=provider,
        oauth_provider_id=provider_id,
        is_active=True,
        is_verified=True,  # OAuth users are pre-verified
        role=UserRole.REGULAR_USER,
        hashed_password=None,  # OAuth users don't have passwords
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    logger.info(f"Created new user via {provider}: {user.email}")

    return user


async def _generate_tokens_for_user(
    db: AsyncSession,
    user: User,
) -> Tuple[str, str]:
    """
    Generate JWT access and refresh tokens for user.

    Args:
        db: Database session
        user: User to generate tokens for

    Returns:
        Tuple of (access_token, refresh_token)
    """
    # Generate tokens
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    refresh_token_str = create_refresh_token(data={"sub": str(user.id)})

    # Store refresh token in database
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    refresh_token = RefreshToken(
        token=hash_token(refresh_token_str),
        user_id=user.id,
        expires_at=expires_at,
    )

    db.add(refresh_token)
    await db.commit()

    return access_token, refresh_token_str
