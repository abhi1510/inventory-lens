import logging
from fastapi import APIRouter, HTTPException

from app.db.session import SessionLocal
from app.schemas.inventory import InventoryUpsert, InventoryResponse
from app.services.inventory_service import InventoryService

log = logging.getLogger(__name__)

router = APIRouter()


@router.put("/inventory", response_model=InventoryResponse)
def upsert_inventory(req: InventoryUpsert):
    session = SessionLocal()

    try:
        service = InventoryService(session)
        inventory = service.upsert_inventory(
            req.product_id,
            req.stock,
            req.min_stock,
        )
        return inventory

    except Exception:
        session.rollback()
        log.exception("Failed to upsert inventory")
        raise HTTPException(status_code=500, detail="Internal error")

    finally:
        session.close()
