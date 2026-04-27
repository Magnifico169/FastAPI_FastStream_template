from datetime import datetime
from uuid import UUID

from sqlalchemy import JSON, Column, String, Uuid, DateTime
from sqlalchemy.orm import MappedColumn

from common.persistence.models.base_table import BaseTable


class Order(BaseTable):
    __tablename__ = "orders"

    products: MappedColumn[object] = Column(JSON(), nullable=False)
    user_id: MappedColumn[UUID] = Column(Uuid(), nullable=False, foreign_key="users.id")
    address: MappedColumn[str] = Column(String(), nullable=False)
    delivery_date: MappedColumn[datetime] = Column(DateTime(), nullable=False)
    description: MappedColumn[str] = Column(String(), nullable=True)
