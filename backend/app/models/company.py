# app/models/company.py
"""
Company SQLAlchemy model.
Represents tech companies posting jobs.
"""

from typing import List, Optional
from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Company(Base):
    """
    Company model representing tech companies.

    Relationships:
        - One company has many jobs (one-to-many)
        - One company is managed by one user (many-to-one, optional)
    """

    __tablename__ = "companies"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Company Information
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    logo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Foreign Key
    managed_by_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,  # Nullable for backward compatibility with existing companies
        index=True
    )

    # Relationships
    jobs: Mapped[List["Job"]] = relationship(
        "Job",
        back_populates="company",
        cascade="all, delete-orphan"
    )

    managed_by: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="companies_managed",
        foreign_keys=[managed_by_id]
    )
    
    def __repr__(self) -> str:
        return f"<Company(id={self.id}, name='{self.name}')>"
