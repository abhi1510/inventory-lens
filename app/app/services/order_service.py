import json
import logging
from sqlalchemy import select

from app.db.models import Inventory, Order
from app.config import settings
from kafka_lib.producer import KafkaProducerClient

log = logging.getLogger(__name__)


class OrderService:
    def __init__(self, session):
        self.session = session
        self.producer = KafkaProducerClient(settings.KAFKA_BOOTSTRAP_SERVERS)

    def get_all_orders(self):
        return self.session.execute(select(Order)).scalars().all()

    def get_order_by_id(self, order_id: int):
        return self.session.execute(
            select(Order).where(Order.id == order_id)
        ).scalar_one_or_none()

    def create_order(self, product_id: str, quantity: int):
        inventory = self.session.execute(
            select(Inventory)
            .where(Inventory.product_id == product_id)
            .with_for_update()
        ).scalar_one_or_none()

        if not inventory:
            log.exception("Product not found")
            raise ValueError("Product not found")

        if inventory.stock < quantity:
            event = {
                "product_id": product_id,
                "stock": inventory.stock,
                "min_stock": inventory.min_stock,
            }

            self.producer.publish(
                topic=settings.KAFKA_TOPIC,
                data=json.dumps(event),
            )
            self.producer.flush()

            log.exception("Insufficient stock")
            raise ValueError("Insufficient stock")

        inventory.stock -= quantity

        order = Order(
            product_id=product_id,
            quantity=quantity,
        )

        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)

        log.info("Order created for product_id=%s", product_id)

        return order
