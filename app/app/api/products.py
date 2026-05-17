import logging
from fastapi import APIRouter, HTTPException

from app.db.session import SessionLocal
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import ProductService

log = logging.getLogger(__name__)

router = APIRouter()


@router.post("/products", response_model=ProductResponse)
def create_product(req: ProductCreate):
    session = SessionLocal()

    try:
        service = ProductService(session)
        product = service.create_product(req.product_id, req.product_name)
        return product

    except Exception:
        session.rollback()
        log.exception("Failed to create product")
        raise HTTPException(status_code=500, detail="Internal error")

    finally:
        session.close()


@router.get("/products", response_model=list[ProductResponse])
def get_all_products():
    session = SessionLocal()

    try:
        service = ProductService(session)
        return service.get_all()

    finally:
        session.close()


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    session = SessionLocal()

    try:
        service = ProductService(session)
        product = service.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    finally:
        session.close()


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: str, req: ProductUpdate):
    session = SessionLocal()

    try:
        service = ProductService(session)
        product = service.update_product(product_id, req.product_name)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product

    finally:
        session.close()
