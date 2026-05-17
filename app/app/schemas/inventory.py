from pydantic import BaseModel


class InventoryUpsert(BaseModel):
    product_id: str
    stock: int
    min_stock: int


class InventoryResponse(BaseModel):
    product_id: str
    stock: int
    min_stock: int

    class Config:
        from_attributes = True
