from pydantic import BaseModel, Field


class Product(BaseModel):
    """
    Product model

    :ivar name: Product name
    :vartype name: str
    :ivar count: Product count
    :vartype count: int
    :ivar price: Product price
    :vartype price: float
    :ivar description: Product description
    :vartype description: str
    """

    name: str = Field(..., description="Product name")
    count: int = Field(..., description="Product count")
    price: float = Field(..., description="Product price")
    description: str = Field(..., description="Product description")
