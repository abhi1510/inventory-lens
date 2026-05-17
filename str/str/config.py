import os
from pathlib import Path


class Settings:
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    DATASET_DIR = Path(__file__).resolve().parent / "datasets"
    RUN_FLASH_SALE = True


settings = Settings()
