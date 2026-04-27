from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str = Field(..., description="Product name")
    count: int = Field(..., description="Product count")
    price: float = Field(..., description="Product price")
    description: str = Field(..., description="Product description")
