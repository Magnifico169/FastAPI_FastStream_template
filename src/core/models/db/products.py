from sqlalchemy.orm import MappedColumn
from sqlalchemy import Column, Integer, String, Float

from base_table import BaseTable


class Products(BaseTable):
    """ORM mapping for the products table.

    :ivar name: Product title.
    :ivar count: Stock quantity.
    :ivar price: Unit price.
    :ivar description: Descriptive text for the product.
    """

    __tablename__ = "products"

    name: MappedColumn[str] = Column(String(), nullable=False)
    count: MappedColumn[int] = Column(Integer(), nullable=False)
    price: MappedColumn[float] = Column(Float(), nullable=False)
    description: MappedColumn[str] = Column(String(), nullable=False)
