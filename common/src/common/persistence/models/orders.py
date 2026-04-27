from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, Column, String, Uuid, DateTime
from sqlalchemy.orm import MappedColumn

from common.persistence.models.base_table import BaseTable


class Order(BaseTable):
    """ORM mapping for the orders table.

    :ivar products: Line items and metadata, stored as JSON.
    :ivar user_id: Reference to the owning user row.
    :ivar address: Delivery address for the order.
    :ivar delivery_date: Scheduled or agreed delivery time.
    :ivar description: Optional free-form notes, null when not set.
    """

    __tablename__ = "orders"

    products: MappedColumn[object] = Column(JSON(), nullable=False)
    user_id: MappedColumn[UUID] = Column(Uuid(), nullable=False)
    address: MappedColumn[str] = Column(String(), nullable=False)
    delivery_date: MappedColumn[datetime] = Column(DateTime(timezone=True), nullable=False)
    description: MappedColumn[str] = Column(String(), nullable=True)
