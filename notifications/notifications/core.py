import smtplib
import logging
from notifications.config import settings
from kafka_lib.consumer import KafkaConsumerClient
from email.mime.text import MIMEText

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
log = logging.getLogger(__name__)


def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = settings.FROM_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.send_message(msg)

        log.info(f"Email sent to {to_email}")

    except Exception as e:
        log.error(f"Failed to send email: {e}", exc_info=True)


def handle_inventory_event(event: dict) -> None:
    product_id = event["product_id"]
    curr_stock = event["stock"]
    min_stock = event["min_stock"]

    log.info(
        "Inventory updated product_id=%s curr_stock=%s min_stock=%s",
        product_id,
        curr_stock,
        min_stock,
    )

    if curr_stock < min_stock:
        log.warning("LOW STOCK ALERT product_id=%s", product_id)
        body = (
            f"Low Stock Alert!\n\n"
            f"Product ID: {product_id}\n"
            f"Current Stock: {curr_stock}\n"
            f"Minimum Stock Threshold: {min_stock}\n\n"
            f"Please restock this product as soon as possible."
        )
        send_email(
            to_email="admin@ilens.com",
            subject=f"Inventory update for product {product_id}",
            body=body,
        )


def main():
    consumer = KafkaConsumerClient(
        settings.KAFKA_BOOTSTRAP_SERVERS,
        settings.KAFKA_GROUP_ID,
        [settings.KAFKA_TOPIC],
    )
    consumer.consume(handler=handle_inventory_event)


if __name__ == "__main__":
    main()
