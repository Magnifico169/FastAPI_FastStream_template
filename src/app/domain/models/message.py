from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.enums.message_status import MessageStatus


class Message(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = None
    text: str
    status: MessageStatus
    created_at: datetime | None = None
