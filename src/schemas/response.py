from typing import Literal

from pydantic import BaseModel, Field

StatusMessageLiteral = Literal["processing", "error", "ok"]


class MessageStatusResponse(BaseModel):
    message: StatusMessageLiteral
    status: int = Field(..., ge=100, le=599)
