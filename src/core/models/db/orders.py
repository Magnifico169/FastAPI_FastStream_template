from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import MappedColumn
from sqlalchemy import JSON, Column, Uuid, String, DateTime

from base_table import BaseTable


class Orders(BaseTable):
    """ORM mapping for the orders table.

    :ivar products: Line items and metadata, stored as JSON.
    :ivar user_id: Reference to the owning user row.
    :ivar address: Delivery address for the order.
    :ivar delivery_date: Scheduled or agreed delivery time.
    :ivar description: Optional free-form notes, null when not set.
    """

    __tablename__ = "orders"

    products: MappedColumn[JSON] = Column(JSON(), nullable=False)
    user_id: MappedColumn[UUID] = Column(Uuid(), nullable=False, foreign_key="users.id")
    address: MappedColumn[str] = Column(String(), nullable=False)
    delivery_date: MappedColumn[datetime] = Column(DateTime(), nullable=False)
    description: MappedColumn[str] = Column(String(), nullable=True)
