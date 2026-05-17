import logging
from fastapi import FastAPI

from app.api.orders import router as order_router
from app.api.products import router as product_router
from app.api.inventory import router as inventory_router

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    force=True,
)

app = FastAPI(title="Services - InventoryLens")

app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(order_router)
