# app/models/oauth_state.py
"""
OAuth state token model for CSRF protection.
"""

from datetime import datetime
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class OAuthState(Base):
    """
    OAuth state token for CSRF protection.
    
    Stores state parameter used in OAuth flow to prevent CSRF attacks.
    State tokens expire after a short period (default 10 minutes).
    """
    __tablename__ = "oauth_states"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    state: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    provider: Mapped[str] = mapped_column(String(20), nullable=False)  # 'google' or 'github'
    used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<OAuthState(state={self.state[:8]}..., provider={self.provider}, used={self.used})>"
