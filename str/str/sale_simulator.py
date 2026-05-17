import json
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class FlashSaleSimulator:
    def __init__(
        self,
        loader,
        products: list,
        endpoint: str = "/orders",
        total_orders: int = 1000,
        max_workers: int = 100,
        spike_factor: int = 5,
        max_quantity_per_order: int = 3,
    ):
        self.loader = loader
        self.products = products
        self.endpoint = endpoint
        self.total_orders = total_orders
        self.max_workers = max_workers
        self.spike_factor = spike_factor
        self.max_quantity_per_order = max_quantity_per_order

        self.success = 0
        self.failed = 0
        self.errors = []

    @staticmethod
    def _random_user_id() -> str:
        return "".join(
            random.choices(
                string.ascii_lowercase + string.digits,
                k=10,
            )
        )

    def _generate_order_payload(self) -> dict:
        product = random.choice(self.products)

        # heavily biased toward quantity=1
        quantity = random.choice([1, 1, 1, 1, 2, 2, 3])
        quantity = min(quantity, self.max_quantity_per_order)

        return {
            "product_id": product["product_id"],
            "quantity": quantity,
        }

    def _submit_order(self) -> dict:
        try:
            response = self.loader.post(
                endpoint=self.endpoint,
                payload=self._generate_order_payload(),
            )

            return {
                "status": "success",
                "response": response,
            }

        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
            }

    def run(self):
        print("🚀 Flash Sale Started")
        print(f"📦 Products Loaded : {len(self.products)}")
        print(f"🛒 Total Orders    : {self.total_orders}")
        print(f"⚡ Max Workers     : {self.max_workers}")
        print(f"🌊 Spike Factor    : {self.spike_factor}")
        print()

        start = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []

            orders_per_spike = max(
                1,
                self.total_orders // self.spike_factor,
            )

            for spike in range(self.spike_factor):
                print(f"🔥 Spike Wave {spike + 1}")

                # simulate burst traffic
                jitter = random.uniform(0.1, 0.8)
                time.sleep(jitter)

                for _ in range(orders_per_spike):
                    futures.append(executor.submit(self._submit_order))

            for future in as_completed(futures):
                result = future.result()

                if result["status"] == "success":
                    self.success += 1
                else:
                    self.failed += 1
                    self.errors.append(result["error"])

        duration = time.time() - start

        print("\n📊 FLASH SALE RESULTS")
        print("----------------------------")
        print(f"✔ Successful Orders : {self.success}")
        print(f"✖ Failed Orders     : {self.failed}")
        print(f"⏱ Total Duration    : {duration:.2f}s")

        if self.errors:
            print(f"⚠ Sample Errors     : {self.errors[:5]}")
