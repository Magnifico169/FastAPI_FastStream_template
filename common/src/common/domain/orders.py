from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from common.domain.product import Product


class Order(BaseModel):
    """Pydantic model aligned with the orders database table."""

    id: UUID = Field(default_factory=uuid4, description="Primary key; generated for new rows when using defaults.")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="UTC instant when the record was first stored."
    )
    products: list[Product] = Field(
        default_factory=list, description="Line items and extra data, matching the database JSON column."
    )
    user_id: UUID = Field(..., description="User who placed the order.")
    address: str = Field(..., description="Destination address for delivery.")
    delivery_date: datetime = Field(..., description="Expected or scheduled delivery time.")
    description: str | None = Field(default=None, description="Free-form notes, absent when the column is null.")
