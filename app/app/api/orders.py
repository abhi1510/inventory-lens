import logging
from fastapi import APIRouter, HTTPException

from app.db.session import SessionLocal
from app.schemas.order import OrderResponse, OrderCreateRequest
from app.services.order_service import OrderService

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/orders", response_model=list[OrderResponse])
def get_all_orders():
    session = SessionLocal()

    try:
        service = OrderService(session)
        return service.get_all_orders()

    finally:
        session.close()


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    session = SessionLocal()

    try:
        service = OrderService(session)
        order = service.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    finally:
        session.close()


@router.post("/orders")
def create_order(req: OrderCreateRequest):
    session = SessionLocal()

    try:
        service = OrderService(session)

        result = service.create_order(
            product_id=req.product_id,
            quantity=req.quantity,
        )

        return {"status": "success", "data": result}

    except ValueError as e:
        session.rollback()

        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        session.rollback()
        log.exception("Unexpected error")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        session.close()
