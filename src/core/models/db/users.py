from sqlalchemy.orm import MappedColumn
from sqlalchemy import Column, String

from base_table import BaseTable


class User(BaseTable):
    """ORM mapping for the users table.

    :ivar nickname: Public or internal name for the user.
    :ivar delivery_address: Default delivery or shipping address.
    :ivar status: Current account or workflow status.
    """

    __tablename__ = "users"

    nickname: MappedColumn[str] = Column(String(), nullable=False)
    delivery_address: MappedColumn[str] = Column(String(), nullable=False)
    status: MappedColumn[str] = Column(String(), nullable=False)
