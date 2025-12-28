# app/models/email_verification_token.py
"""
EmailVerificationToken SQLAlchemy model.
Manages email verification tokens for user registration.
"""

from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EmailVerificationToken(Base):
    """
    EmailVerificationToken model for email verification during registration.

    Token is sent to user's email and must be used to activate account.
    Tokens expire after a configured time period (default: 24 hours).

    Relationships:
        - Many verification tokens belong to one user (many-to-one)

    Indexes:
        - token: For fast token lookup (unique)
        - user_id: For user-specific queries
    """

    __tablename__ = "email_verification_tokens"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Token Information
    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    # Foreign Key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Token Status
    used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # Expiration
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
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
        back_populates="email_verification_tokens"
    )

    def __repr__(self) -> str:
        return f"<EmailVerificationToken(id={self.id}, user_id={self.user_id}, used={self.used})>"
