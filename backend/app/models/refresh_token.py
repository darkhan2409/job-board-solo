# app/models/refresh_token.py
"""
RefreshToken SQLAlchemy model.
Manages refresh token rotation for secure JWT authentication.
"""

from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Boolean, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RefreshToken(Base):
    """
    RefreshToken model for JWT token rotation.

    Implements refresh token rotation strategy for enhanced security.
    When a refresh token is used, it's revoked and a new one is issued.

    Relationships:
        - Many refresh tokens belong to one user (many-to-one)

    Indexes:
        - token: For fast token lookup (hashed)
        - user_id: For user-specific queries
        - expires_at: For cleanup of expired tokens
    """

    __tablename__ = "refresh_tokens"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Token Information
    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )  # Hashed token value

    # Foreign Key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Token Status
    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # Expiration
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True
    )

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens"
    )

    # Composite indexes for common query patterns
    __table_args__ = (
        Index("ix_refresh_tokens_user_revoked", "user_id", "revoked"),
    )

    def __repr__(self) -> str:
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.revoked})>"
