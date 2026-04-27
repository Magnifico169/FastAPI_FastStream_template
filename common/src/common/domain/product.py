from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Product(BaseModel):
    """Pydantic model aligned with the products database table."""

    id: UUID = Field(default_factory=uuid4, description="Primary key; generated for new rows when using defaults.")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="UTC instant when the record was first stored."
    )
    name: str = Field(..., description="Human-readable product title.")
    count: int = Field(..., description="Available quantity in stock.")
    price: float = Field(..., description="Unit price in the application currency.")
    description: str = Field(..., description="Marketing or technical copy for the product.")
