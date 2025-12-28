# app/models/user.py
"""
User SQLAlchemy model.
Represents users with authentication and authorization capabilities.
"""

import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(str, enum.Enum):
    """
    User role enumeration for RBAC (Role-Based Access Control).
    Enforces valid role values at database level.
    """
    REGULAR_USER = "regular_user"
    EMPLOYER = "employer"
    ADMIN = "admin"


class User(Base):
    """
    User model representing authenticated users.

    Supports multiple authentication methods:
    - Email/password (local authentication)
    - OAuth (Google, GitHub)

    Relationships:
        - One user can create many jobs (one-to-many)
        - One user can manage many companies (one-to-many)
        - One user can save many jobs (many-to-many via SavedJob)
        - One user can have many refresh tokens (one-to-many)

    Indexes:
        - email: Unique constraint for login
        - is_active: For filtering active users
        - role: For role-based queries
        - oauth_provider_id: For OAuth user lookup
    """

    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Authentication Information
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    hashed_password: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True  # Nullable for OAuth users
    )

    # User Information
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)

    # Role & Status
    role: Mapped[UserRole] = mapped_column(
        String(20),  # Using String instead of Enum for better SQLite compatibility
        default=UserRole.REGULAR_USER,
        nullable=False,
        index=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # OAuth Information
    oauth_provider: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )  # 'google', 'github', or None for local auth
    oauth_provider_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    jobs_created: Mapped[List["Job"]] = relationship(
        "Job",
        back_populates="created_by",
        foreign_keys="Job.created_by_id",
        cascade="all, delete-orphan"
    )

    companies_managed: Mapped[List["Company"]] = relationship(
        "Company",
        back_populates="managed_by",
        foreign_keys="Company.managed_by_id",
        cascade="all, delete-orphan"
    )

    saved_jobs: Mapped[List["SavedJob"]] = relationship(
        "SavedJob",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    email_verification_tokens: Mapped[List["EmailVerificationToken"]] = relationship(
        "EmailVerificationToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    password_reset_tokens: Mapped[List["PasswordResetToken"]] = relationship(
        "PasswordResetToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Composite indexes for common query patterns
    __table_args__ = (
        Index("ix_users_email_active", "email", "is_active"),
        Index("ix_users_oauth_provider", "oauth_provider", "oauth_provider_id"),
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role={self.role})>"
