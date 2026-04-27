from sqlalchemy import Column, String
from sqlalchemy.orm import MappedColumn

from common.persistence.models.base_table import BaseTable


class User(BaseTable):
    __tablename__ = "users"

    nickname: MappedColumn[str] = Column(String(), nullable=False)
    delivery_address: MappedColumn[str] = Column(String(), nullable=False)
    status: MappedColumn[str] = Column(String(), nullable=False)
