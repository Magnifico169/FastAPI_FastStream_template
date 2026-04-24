from uuid import UUID

from pydantic import BaseModel, Field

from constants.user_status import UserStatus


class UserInfoSchema(BaseModel):
    """
    User Info model

    :ivar user_id: User ID
    :ivar status: User Status
    """

    user_id: UUID = Field(..., description="User ID")
    status: UserStatus = Field(..., description="Order Status")
