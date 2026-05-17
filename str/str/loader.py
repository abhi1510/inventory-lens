import json
import requests
import logging

from str.config import settings

log = logging.getLogger(__name__)


class APILoader:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = settings.BASE_URL
        self.dataset_dir = settings.DATASET_DIR

    def _request(
        self,
        method: str,
        endpoint: str,
        payload: dict,
    ) -> requests.Response:
        url = f"{self.base_url}{endpoint}"

        response = self.session.request(
            method=method,
            url=url,
            json=payload,
            timeout=5,
        )

        return response

    def _bulk_request(
        self,
        method: str,
        endpoint: str,
        payload: list[dict],
    ) -> dict:
        results = {
            "success": 0,
            "failed": 0,
        }

        for item in payload:
            try:
                response = self._request(
                    method=method,
                    endpoint=endpoint,
                    payload=item,
                )

                if response.ok:
                    log.info(
                        "✅ %s success: %s",
                        method,
                        item,
                    )
                    results["success"] += 1

                else:
                    log.warning(
                        "❌ %s failed: %s -> %s",
                        method,
                        item,
                        response.text,
                    )
                    results["failed"] += 1

            except requests.exceptions.RequestException:
                log.exception(
                    "❌ %s request error: %s",
                    method,
                    item,
                )
                results["failed"] += 1

        return results

    def post(self, endpoint: str, payload: dict):
        response = self._request(
            method="POST",
            endpoint=endpoint,
            payload=payload,
        )

        response.raise_for_status()

        log.info("✅ POST success: %s", payload)

        return response.json()

    def put(self, endpoint: str, payload: dict):
        response = self._request(
            method="PUT",
            endpoint=endpoint,
            payload=payload,
        )

        response.raise_for_status()

        log.info("✅ PUT success: %s", payload)

        return response.json()

    def load_dataset(self, filename: str):
        file_path = self.dataset_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Dataset not found: {file_path}")

        with open(file_path, "r") as f:
            return json.load(f)

    def post_many(
        self,
        endpoint: str,
        payload: list[dict],
    ) -> dict:
        return self._bulk_request(
            method="POST",
            endpoint=endpoint,
            payload=payload,
        )

    def put_many(
        self,
        endpoint: str,
        payload: list[dict],
    ) -> dict:
        return self._bulk_request(
            method="PUT",
            endpoint=endpoint,
            payload=payload,
        )
