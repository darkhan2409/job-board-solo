# app/models/saved_job.py
"""
SavedJob SQLAlchemy model.
Junction table for many-to-many relationship between users and jobs.
"""

from datetime import datetime
from sqlalchemy import Integer, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SavedJob(Base):
    """
    SavedJob model for user's saved/bookmarked jobs.

    Implements a many-to-many relationship between Users and Jobs.
    Allows users to save jobs for later viewing.

    Relationships:
        - Many saved jobs belong to one user (many-to-one)
        - Many saved jobs reference one job (many-to-one)

    Indexes:
        - Composite primary key (user_id, job_id)
        - user_id: For fetching all saved jobs for a user
        - job_id: For checking if a job is saved
        - saved_at: For sorting by save date
    """

    __tablename__ = "saved_jobs"

    # Composite Primary Key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    job_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("jobs.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Timestamp
    saved_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="saved_jobs"
    )

    job: Mapped["Job"] = relationship(
        "Job",
        back_populates="saved_by_users"
    )

    # Composite index for common query patterns
    __table_args__ = (
        Index("ix_saved_jobs_user_saved_at", "user_id", "saved_at"),
    )

    def __repr__(self) -> str:
        return f"<SavedJob(user_id={self.user_id}, job_id={self.job_id})>"
