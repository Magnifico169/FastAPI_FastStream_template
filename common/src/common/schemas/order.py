from uuid import UUID

from pydantic import BaseModel, Field

from common.constants.order_status import OrderStatus


class OrderStatusRequestSchema(BaseModel):
    order_id: UUID = Field(..., description="Order ID")
    user_id: UUID = Field(..., description="User ID")
