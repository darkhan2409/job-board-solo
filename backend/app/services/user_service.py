# app/services/user_service.py
"""
User service for profile management operations.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.email_verification_token import EmailVerificationToken
from app.utils.security import hash_password, verify_password, generate_random_token
from app.utils.exceptions import NotFoundException, ValidationException
from app.services.email_service import send_verification_email
from app.config import settings

logger = logging.getLogger(__name__)


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Get user by ID.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        User or None if not found
    """
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Get user by email address.

    Args:
        db: Database session
        email: User's email

    Returns:
        User or None if not found
    """
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_user_profile(
    db: AsyncSession,
    user: User,
    full_name: Optional[str] = None,
    email: Optional[str] = None,
) -> User:
    """
    Update user profile information.

    Args:
        db: Database session
        user: User to update
        full_name: New full name (optional)
        email: New email address (optional)

    Returns:
        Updated user

    Raises:
        ValidationException: If email already exists
    """
    # Update full name
    if full_name is not None:
        user.full_name = full_name

    # Update email (check uniqueness)
    if email is not None and email != user.email:
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ValidationException("Email already in use")

        # Store old email for logging
        old_email = user.email
        
        # Update email and require re-verification
        user.email = email
        user.is_verified = False
        
        # Generate email verification token
        token = generate_random_token()
        expires_at = datetime.utcnow() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)

        verification_token = EmailVerificationToken(
            token=token,
            user_id=user.id,
            expires_at=expires_at,
        )

        db.add(verification_token)
        await db.flush()  # Ensure token is saved before sending email

        # Send verification email to new address
        try:
            await send_verification_email(
                email=user.email,
                full_name=user.full_name,
                verification_token=token,
            )
            logger.info(f"User {user.id} changed email from {old_email} to {email} - verification email sent")
        except Exception as e:
            logger.error(f"Failed to send verification email to {email}: {e}")
            # Don't fail the entire operation if email fails
            # User can request a new verification email later

    await db.commit()
    await db.refresh(user)

    logger.info(f"User profile updated for user {user.id}")

    return user


async def change_password(
    db: AsyncSession,
    user: User,
    current_password: str,
    new_password: str,
) -> User:
    """
    Change user's password.

    Args:
        db: Database session
        user: User whose password to change
        current_password: Current password (for verification)
        new_password: New password

    Returns:
        Updated user

    Raises:
        ValidationException: If current password is incorrect
    """
    # Verify current password
    if not user.hashed_password:
        raise ValidationException("Cannot change password for OAuth users")

    if not verify_password(current_password, user.hashed_password):
        raise ValidationException("Current password is incorrect")

    # Update password
    user.hashed_password = hash_password(new_password)

    await db.commit()
    await db.refresh(user)

    logger.info(f"Password changed for user {user.id}")

    return user


async def deactivate_user(db: AsyncSession, user: User) -> User:
    """
    Deactivate user account.

    Args:
        db: Database session
        user: User to deactivate

    Returns:
        Deactivated user
    """
    user.is_active = False

    await db.commit()
    await db.refresh(user)

    logger.info(f"User {user.id} deactivated")

    return user


async def reactivate_user(db: AsyncSession, user: User) -> User:
    """
    Reactivate user account.

    Args:
        db: Database session
        user: User to reactivate

    Returns:
        Reactivated user
    """
    user.is_active = True

    await db.commit()
    await db.refresh(user)

    logger.info(f"User {user.id} reactivated")

    return user
