from sqlalchemy import Column, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import MappedColumn

from common.persistence.models.base_table import BaseTable


class Product(BaseTable):
    """ORM mapping for the products table.

    :ivar name: Product title.
    :ivar count: Stock quantity.
    :ivar price: Unit price.
    :ivar description: Descriptive text for the product.
    """

    __tablename__ = "products"

    __table_args__ = (UniqueConstraint("name", "price", "created_at", name="uq_products_name_price_created_at"),)

    name: MappedColumn[str] = Column(String(), nullable=False)
    count: MappedColumn[int] = Column(Integer(), nullable=False)
    price: MappedColumn[float] = Column(Float(), nullable=False)
    description: MappedColumn[str] = Column(String(), nullable=False)
