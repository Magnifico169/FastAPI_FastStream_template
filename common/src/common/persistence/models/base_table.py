from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, Uuid
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, MappedColumn


class Base(AsyncAttrs, DeclarativeBase):
    """Base declarative class for the ORM."""


class BaseTable(Base):
    """
    Abstract table with shared primary key and creation timestamp.

    :ivar id: Unique primary key for the table.
    :ivar created_at: UTC timestamp for the table.
    """

    __abstract__ = True

    id: MappedColumn[UUID] = Column(Uuid(), primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC), nullable=False)
