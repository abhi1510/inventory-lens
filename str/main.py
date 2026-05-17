import logging

from str.config import settings
from str.loader import APILoader
from str.sale_simulator import FlashSaleSimulator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
log = logging.getLogger("main")

loader = APILoader()


def run_flash_sale(products: list[dict]):
    simulator = FlashSaleSimulator(
        loader=loader,
        products=products,
        endpoint="/orders",
        total_orders=10000,
        max_workers=10,
        spike_factor=50,
        max_quantity_per_order=3,
    )

    simulator.run()


def main():
    products = loader.load_dataset("products.json")
    inventory = loader.load_dataset("inventory.json")
    products_result = loader.post_many(endpoint="/products", payload=products)
    inventory_result = loader.put_many(endpoint="/inventory", payload=inventory)

    if settings.RUN_FLASH_SALE:
        run_flash_sale(products)

    print("Products Summary:", products_result)
    print("Inventory Summary:", inventory_result)


if __name__ == "__main__":
    main()
