import logging
from sqlalchemy import select

from app.db.models import Product, Inventory

log = logging.getLogger(__name__)


class ProductService:
    def __init__(self, session):
        self.session = session

    def create_product(self, product_id: str, product_name: str | None):
        product = Product(
            product_id=product_id,
            product_name=product_name,
        )
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        log.info("Product created product_id=%s", product_id)

        return product

    def get_all(self):
        return self.session.execute(select(Product)).scalars().all()

    def get_by_id(self, product_id: str):
        return self.session.execute(
            select(Product).where(Product.product_id == product_id)
        ).scalar_one_or_none()

    def update_product(self, product_id: str, product_name: str | None):
        product = self.session.execute(
            select(Product).where(Product.product_id == product_id)
        ).scalar_one_or_none()

        if not product:
            return None

        if product_name is not None:
            product.product_name = product_name

        self.session.commit()
        self.session.refresh(product)

        log.info("Product updated product_id=%s", product_id)

        return product
