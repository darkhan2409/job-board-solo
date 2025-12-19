# app/models/job.py
"""
Job SQLAlchemy model.
Represents job postings with company relationships.
"""

import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, ForeignKey, Enum, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class JobLevel(str, enum.Enum):
    """
    Job seniority level enumeration.
    Enforces valid values at database level.
    """
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"


class Job(Base):
    """
    Job model representing job postings.
    
    Relationships:
        - Many jobs belong to one company (many-to-one)
        
    Indexes:
        - location: For location-based filtering
        - level: For seniority level filtering
        - created_at: For sorting by date
        - company_id: For company-based queries (foreign key auto-indexed)
    """
    
    __tablename__ = "jobs"
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Job Information
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    salary: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    level: Mapped[JobLevel] = mapped_column(
        Enum(JobLevel),
        nullable=False,
        index=True
    )
    
    # Foreign Key
    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    
    # Relationships
    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="jobs"
    )
    
    # Composite indexes for common query patterns
    __table_args__ = (
        Index("ix_jobs_location_level", "location", "level"),
        Index("ix_jobs_company_created", "company_id", "created_at"),
    )
    
    def __repr__(self) -> str:
        return f"<Job(id={self.id}, title='{self.title}', level={self.level.value})>"
