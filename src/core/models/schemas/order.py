from uuid import UUID

from pydantic import BaseModel, Field

from constants.order_status import OrderStatus


class OrderStatusRequestSchema(BaseModel):
    """
    Order Status Request model

    :ivar order_id: Order ID
    :vartype order_id: UUID
    :ivar user_id: User ID
    :vartype user_id: UUID
    """

    order_id: UUID = Field(..., description="Order ID")
    user_id: UUID = Field(..., description="User ID")
