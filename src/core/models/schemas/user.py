from uuid import UUID

from pydantic import BaseModel, Field

from constants.user_status import UserStatus


class UserInfoSchema(BaseModel):
    """
    User Info model

    :ivar user_id: User ID
    :vartype user_id: UUID
    :ivar nickname: User Nickname
    :vartype nickname: str
    :ivar delivery_address: User Delivery Address
    :vartype delivery_address: str
    :ivar status: User Status
    :vartype status: UserStatus
    """

    user_id: UUID = Field(..., description="User ID")
    nickname: str = Field(..., description="Public or internal display name for the user.")
    delivery_address: str = Field(..., description="Default shipping or hand-off address.")
    status: UserStatus = Field(..., description="Order Status")
