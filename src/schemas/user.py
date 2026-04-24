from uuid import UUID
from enum import StrEnum

from pydantic import BaseModel, Field


class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"


class UserInfoSchema(BaseModel):
    """
    User Info model

    :ivar user_id: User ID
    :ivar status: User Status
    """

    user_id: UUID = Field(..., description="User ID")
    status: UserStatus = Field(..., description="Order Status")
