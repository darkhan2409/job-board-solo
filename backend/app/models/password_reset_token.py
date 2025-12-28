# app/models/password_reset_token.py
"""
PasswordResetToken SQLAlchemy model.
Manages password reset tokens for account recovery.
"""

from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PasswordResetToken(Base):
    """
    PasswordResetToken model for password reset functionality.

    Token is sent to user's email and allows them to reset their password.
    Tokens expire after a short time period (default: 1 hour) for security.

    Relationships:
        - Many reset tokens belong to one user (many-to-one)

    Indexes:
        - token: For fast token lookup (unique)
        - user_id: For user-specific queries
    """

    __tablename__ = "password_reset_tokens"

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
        back_populates="password_reset_tokens"
    )

    def __repr__(self) -> str:
        return f"<PasswordResetToken(id={self.id}, user_id={self.user_id}, used={self.used})>"
