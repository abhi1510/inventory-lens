from confluent_kafka import Producer
import socket
import logging

log = logging.getLogger(__name__)


class KafkaProducerClient:
    def __init__(self, kafka_bootstrap_servers) -> None:
        self._producer = Producer(
            {
                "bootstrap.servers": kafka_bootstrap_servers,
                "client.id": socket.gethostname(),
            }
        )

    @staticmethod
    def _delivery_report(err, msg) -> None:
        if err is not None:
            log.error(
                "Failed to deliver message to topic=%s: %s",
                msg.topic() if msg else "unknown",
                err,
            )
            return

        log.info(
            "Message delivered topic=%s partition=%s offset=%s",
            msg.topic(),
            msg.partition(),
            msg.offset(),
        )

    def publish(
        self,
        topic: str,
        data: bytes,
        key: str | None = None,
    ) -> None:
        try:
            self._producer.produce(
                topic=topic,
                key=key,
                value=data,
                callback=self._delivery_report,
            )

            # Trigger delivery callbacks
            self._producer.poll(0)

            log.info("Event published topic=%s key=%s", topic, key)

        except Exception:
            log.exception("Failed to publish event topic=%s event=%s", topic, data)

    def flush(self, timeout: float = 10) -> None:
        remaining = self._producer.flush(timeout)

        if remaining > 0:
            log.warning(
                "Producer flush completed with %s undelivered messages",
                remaining,
            )
