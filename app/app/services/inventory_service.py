import json
import logging
from sqlalchemy import select
from app.db.models import Inventory
from app.config import settings
from kafka_lib.producer import KafkaProducerClient

log = logging.getLogger(__name__)


class InventoryService:
    def __init__(self, session):
        self.session = session
        self.producer = KafkaProducerClient(settings.KAFKA_BOOTSTRAP_SERVERS)

    def upsert_inventory(self, product_id: str, stock: int, min_stock: int):
        inventory = self.session.execute(
            select(Inventory).where(Inventory.product_id == product_id)
        ).scalar_one_or_none()

        # CASE 1: EXISTS → update
        if inventory:
            inventory.stock = stock
            inventory.min_stock = min_stock

            log.info(
                "Inventory updated product_id=%s stock=%s min_stock=%s",
                product_id,
                stock,
                min_stock,
            )

        # CASE 2: NOT EXISTS → insert
        else:
            inventory = Inventory(
                product_id=product_id,
                stock=stock,
                min_stock=min_stock,
            )
            self.session.add(inventory)

            log.info(
                "Inventory created product_id=%s stock=%s min_stock=%s",
                product_id,
                stock,
                min_stock,
            )

        self.session.commit()
        self.session.refresh(inventory)

        event = {
            "product_id": product_id,
            "stock": stock,
            "min_stock": min_stock,
        }

        self.producer.publish(
            topic=settings.KAFKA_TOPIC,
            data=json.dumps(event),
        )
        self.producer.flush()

        return inventory
