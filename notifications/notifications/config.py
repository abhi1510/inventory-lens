import os


class Settings:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_TOPIC = os.getenv("TOPIC")
    KAFKA_GROUP_ID = os.getenv("GROUP_ID")

    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = os.getenv("SMTP_PORT")
    FROM_EMAIL = os.getenv("FROM_EMAIL")


settings = Settings()
