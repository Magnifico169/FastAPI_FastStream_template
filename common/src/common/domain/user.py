from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class User(BaseModel):
    """Pydantic model aligned with the users database table.

    :ivar id: Primary key; generated for new rows when using defaults.
    :ivar created_at: UTC instant when the record was first stored.
    :ivar nickname: Public or internal display name for the user.
    :ivar delivery_address: Default shipping or hand-off address.
    :ivar status: Current lifecycle or verification state of the user.
    """

    id: UUID = Field(default_factory=uuid4, description="Primary key; generated for new rows when using defaults.")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="UTC instant when the record was first stored."
    )
    nickname: str = Field(..., description="Public or internal display name for the user.")
    delivery_address: str = Field(..., description="Default shipping or hand-off address.")
    status: str = Field(..., description="Current lifecycle or verification state of the user.")
