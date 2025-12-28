# app/services/user_service.py
"""
User service for profile management operations.
"""

import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.security import hash_password, verify_password
from app.utils.exceptions import NotFoundException, ValidationException

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

        # TODO: In production, should send verification email to new address
        user.email = email
        user.is_verified = False  # Require re-verification
        logger.warning(f"User {user.id} changed email to {email} - verification required")

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
