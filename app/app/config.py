import os


class Settings:
    DB_URI = os.getenv("DB_URI")
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_TOPIC = os.getenv("TOPIC")


settings = Settings()
