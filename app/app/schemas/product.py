from pydantic import BaseModel


class ProductCreate(BaseModel):
    product_id: str
    product_name: str | None = None


class ProductUpdate(BaseModel):
    product_name: str | None = None


class ProductResponse(BaseModel):
    id: int
    product_id: str
    product_name: str | None

    class Config:
        from_attributes = True
