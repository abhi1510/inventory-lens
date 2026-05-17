from datetime import datetime
from pydantic import BaseModel


class OrderCreateRequest(BaseModel):
    product_id: str
    quantity: int


class OrderResponse(BaseModel):
    id: int
    product_id: str
    quantity: int
    ordered_at: datetime
