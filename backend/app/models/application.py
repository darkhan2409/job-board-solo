# app/models/application.py
"""
Application SQLAlchemy model.
Represents a job application submitted by a user.
"""

from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum, Text, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ApplicationStatus(str, PyEnum):
    """Application status enum."""
    PENDING = "pending"
    REVIEWING = "reviewing"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"


class Application(Base):
    """
    Application model for job applications.

    Represents a job application submitted by a job seeker to a job posting.

    Relationships:
        - Many applications belong to one user (many-to-one)
        - Many applications belong to one job (many-to-one)

    Indexes:
        - user_id: For fetching all applications by a user
        - job_id: For fetching all applications for a job
        - status: For filtering by status
        - applied_at: For sorting by application date
    """

    __tablename__ = "applications"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Foreign Keys
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    job_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Application Details
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.PENDING,
        nullable=False,
        index=True
    )

    cover_letter: Mapped[str | None] = mapped_column(Text, nullable=True)

    resume_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Timestamps
    applied_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="applications"
    )

    job: Mapped["Job"] = relationship(
        "Job",
        back_populates="applications"
    )

    # Composite indexes for common query patterns
    __table_args__ = (
        Index("ix_applications_user_applied_at", "user_id", "applied_at"),
        Index("ix_applications_job_status", "job_id", "status"),
        Index("ix_applications_unique_user_job", "user_id", "job_id", unique=True),
    )

    def __repr__(self) -> str:
        return f"<Application(id={self.id}, user_id={self.user_id}, job_id={self.job_id}, status={self.status})>"
