# app/services/auth_service.py
"""
Authentication service with business logic for:
- User registration with email verification
- Email verification and account activation
- Login with JWT token generation
- Refresh token rotation
- Logout with token revocation
- Password reset flow
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User, UserRole
from app.models.refresh_token import RefreshToken
from app.models.email_verification_token import EmailVerificationToken
from app.models.password_reset_token import PasswordResetToken
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
from app.utils.exceptions import ValidationException, NotFoundException
from app.services.email_service import (
    send_verification_email,
    send_password_reset_email,
    send_welcome_email,
)

logger = logging.getLogger(__name__)


async def register_user(
    db: AsyncSession,
    email: str,
    password: str,
    full_name: str,
    role: UserRole = UserRole.REGULAR_USER
) -> User:
    """
    Register a new user and send verification email.

    Args:
        db: Database session
        email: User's email address
        password: Plain text password
        full_name: User's full name
        role: User role (default: REGULAR_USER)

    Returns:
        Created user (not yet verified)

    Raises:
        ValidationException: If email already exists
    """
    # Check if email already exists
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise ValidationException("Email already registered")

    # Create user
    user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
        role=role,
        is_active=True,
        is_verified=False,  # Email verification required
    )

    db.add(user)
    await db.flush()  # Get user.id

    # Generate email verification token
    token = generate_random_token()
    expires_at = datetime.utcnow() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)

    verification_token = EmailVerificationToken(
        token=token,
        user_id=user.id,
        expires_at=expires_at,
    )

    db.add(verification_token)
    await db.commit()
    await db.refresh(user)

    # Send verification email (non-blocking)
    try:
        await send_verification_email(
            email=user.email,
            full_name=user.full_name,
            verification_token=token,
        )
        logger.info(f"Verification email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send verification email to {email}: {e}")

    return user


async def verify_email(db: AsyncSession, token: str) -> User:
    """
    Verify user's email address using verification token.

    Args:
        db: Database session
        token: Email verification token

    Returns:
        Verified user

    Raises:
        ValidationException: If token is invalid, expired, or already used
    """
    # Find token
    stmt = select(EmailVerificationToken).where(
        EmailVerificationToken.token == token
    )
    result = await db.execute(stmt)
    verification_token = result.scalar_one_or_none()

    if not verification_token:
        raise ValidationException("Invalid verification token")

    if verification_token.used:
        raise ValidationException("Verification token already used")

    if verification_token.expires_at < datetime.utcnow():
        raise ValidationException("Verification token expired")

    # Get user
    stmt = select(User).where(User.id == verification_token.user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise NotFoundException("User not found")

    # Mark user as verified
    user.is_verified = True
    verification_token.used = True

    await db.commit()
    await db.refresh(user)

    # Send welcome email (non-blocking)
    try:
        await send_welcome_email(
            email=user.email,
            full_name=user.full_name,
        )
        logger.info(f"Welcome email sent to {user.email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user.email}: {e}")

    return user


async def login(
    db: AsyncSession,
    email: str,
    password: str,
    remember_me: bool = False
) -> Tuple[str, str, User]:
    """
    Authenticate user and generate JWT tokens.

    Args:
        db: Database session
        email: User's email
        password: Plain text password
        remember_me: If True, refresh token expires in 90 days instead of 30

    Returns:
        Tuple of (access_token, refresh_token, user)

    Raises:
        ValidationException: If credentials are invalid or account not verified
    """
    # Find user
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise ValidationException("Invalid email or password")

    if not user.is_active:
        raise ValidationException("Account is deactivated")

    if not user.is_verified:
        raise ValidationException("Email not verified. Please check your inbox.")

    # Generate tokens
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    refresh_token_str = create_refresh_token(
        data={"sub": str(user.id)},
        remember_me=remember_me
    )

    # Store refresh token in database (hashed)
    expires_days = (
        settings.REFRESH_TOKEN_REMEMBER_ME_EXPIRE_DAYS
        if remember_me
        else settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    expires_at = datetime.utcnow() + timedelta(days=expires_days)

    refresh_token = RefreshToken(
        token=hash_token(refresh_token_str),
        user_id=user.id,
        expires_at=expires_at,
    )

    db.add(refresh_token)
    await db.commit()

    logger.info(f"User {user.email} logged in successfully")

    return access_token, refresh_token_str, user


async def refresh_access_token(
    db: AsyncSession,
    refresh_token_str: str
) -> Tuple[str, str]:
    """
    Refresh access token using refresh token (with token rotation).

    Args:
        db: Database session
        refresh_token_str: Refresh token from client

    Returns:
        Tuple of (new_access_token, new_refresh_token)

    Raises:
        ValidationException: If refresh token is invalid or revoked
    """
    # Decode refresh token
    payload = decode_token(refresh_token_str)
    if not payload:
        raise ValidationException("Invalid refresh token")

    user_id = int(payload.get("sub"))

    # Find refresh token in database
    stmt = select(RefreshToken).where(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked == False,  # noqa: E712
    )
    result = await db.execute(stmt)
    tokens = result.scalars().all()

    # Verify token hash
    valid_token = None
    for token in tokens:
        if verify_token_hash(refresh_token_str, token.token):
            valid_token = token
            break

    if not valid_token:
        raise ValidationException("Refresh token not found or revoked")

    if valid_token.expires_at < datetime.utcnow():
        raise ValidationException("Refresh token expired")

    # Get user
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not user.is_active or not user.is_verified:
        raise ValidationException("User not found or inactive")

    # Token rotation: revoke old token and create new one
    valid_token.revoked = True

    # Generate new tokens
    new_access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    new_refresh_token_str = create_refresh_token(data={"sub": str(user.id)})

    # Store new refresh token
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    new_refresh_token = RefreshToken(
        token=hash_token(new_refresh_token_str),
        user_id=user.id,
        expires_at=expires_at,
    )

    db.add(new_refresh_token)
    await db.commit()

    logger.info(f"Tokens refreshed for user {user.email}")

    return new_access_token, new_refresh_token_str


async def logout(db: AsyncSession, refresh_token_str: str) -> None:
    """
    Logout user by revoking refresh token.

    Args:
        db: Database session
        refresh_token_str: Refresh token to revoke

    Raises:
        ValidationException: If token is invalid
    """
    # Decode token to get user_id
    payload = decode_token(refresh_token_str)
    if not payload:
        raise ValidationException("Invalid refresh token")

    user_id = int(payload.get("sub"))

    # Find and revoke token
    stmt = select(RefreshToken).where(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked == False,  # noqa: E712
    )
    result = await db.execute(stmt)
    tokens = result.scalars().all()

    # Verify and revoke token
    for token in tokens:
        if verify_token_hash(refresh_token_str, token.token):
            token.revoked = True
            await db.commit()
            logger.info(f"User {user_id} logged out successfully")
            return

    raise ValidationException("Refresh token not found")


async def request_password_reset(db: AsyncSession, email: str) -> None:
    """
    Generate password reset token and send email.

    Args:
        db: Database session
        email: User's email address

    Note:
        Does not raise exception if email not found (security: don't reveal user existence)
    """
    # Find user
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        # Don't reveal that email doesn't exist
        logger.warning(f"Password reset requested for non-existent email: {email}")
        return

    # Generate password reset token
    token = generate_random_token()
    expires_at = datetime.utcnow() + timedelta(hours=settings.PASSWORD_RESET_EXPIRE_HOURS)

    reset_token = PasswordResetToken(
        token=token,
        user_id=user.id,
        expires_at=expires_at,
    )

    db.add(reset_token)
    await db.commit()

    # Send password reset email
    try:
        await send_password_reset_email(
            email=user.email,
            full_name=user.full_name,
            reset_token=token,
        )
        logger.info(f"Password reset email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send password reset email to {email}: {e}")


async def reset_password(db: AsyncSession, token: str, new_password: str) -> User:
    """
    Reset user's password using reset token.

    Args:
        db: Database session
        token: Password reset token
        new_password: New plain text password

    Returns:
        Updated user

    Raises:
        ValidationException: If token is invalid, expired, or already used
    """
    # Find token
    stmt = select(PasswordResetToken).where(
        PasswordResetToken.token == token
    )
    result = await db.execute(stmt)
    reset_token = result.scalar_one_or_none()

    if not reset_token:
        raise ValidationException("Invalid password reset token")

    if reset_token.used:
        raise ValidationException("Password reset token already used")

    if reset_token.expires_at < datetime.utcnow():
        raise ValidationException("Password reset token expired")

    # Get user
    stmt = select(User).where(User.id == reset_token.user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise NotFoundException("User not found")

    # Update password
    user.hashed_password = hash_password(new_password)
    reset_token.used = True

    # Revoke all refresh tokens for security
    stmt = select(RefreshToken).where(
        RefreshToken.user_id == user.id,
        RefreshToken.revoked == False,  # noqa: E712
    )
    result = await db.execute(stmt)
    refresh_tokens = result.scalars().all()

    for rt in refresh_tokens:
        rt.revoked = True

    await db.commit()
    await db.refresh(user)

    logger.info(f"Password reset successful for user {user.email}")

    return user


async def resend_verification_email(db: AsyncSession, email: str) -> None:
    """
    Resend verification email to user.

    Args:
        db: Database session
        email: User's email address

    Raises:
        ValidationException: If user not found or already verified
    """
    # Find user
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise ValidationException("User not found")

    if user.is_verified:
        raise ValidationException("Email already verified")

    # Generate new verification token
    token = generate_random_token()
    expires_at = datetime.utcnow() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)

    verification_token = EmailVerificationToken(
        token=token,
        user_id=user.id,
        expires_at=expires_at,
    )

    db.add(verification_token)
    await db.commit()

    # Send verification email
    try:
        await send_verification_email(
            email=user.email,
            full_name=user.full_name,
            verification_token=token,
        )
        logger.info(f"Verification email resent to {email}")
    except Exception as e:
        logger.error(f"Failed to resend verification email to {email}: {e}")
        raise ValidationException("Failed to send verification email")
