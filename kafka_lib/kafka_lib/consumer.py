import json
import logging
import signal
from typing import Callable

from confluent_kafka import Consumer, KafkaException, Message

log = logging.getLogger(__name__)


class KafkaConsumerClient:
    def __init__(
        self,
        kafka_bootstrap_servers: str,
        group_id: str,
        topics: list[str],
    ) -> None:
        self._running = True

        self._consumer = Consumer(
            {
                "bootstrap.servers": kafka_bootstrap_servers,
                "group.id": group_id,
                "auto.offset.reset": "earliest",
                "enable.auto.commit": True,
            }
        )

        self._consumer.subscribe(topics)

        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)

        log.info(
            "Kafka consumer initialized topics=%s group_id=%s",
            topics,
            group_id,
        )

    def _shutdown(self, *_args) -> None:
        log.info("Shutdown signal received")
        self._running = False

    @staticmethod
    def _deserialize_message(msg: Message) -> dict:
        try:
            return json.loads(msg.value().decode("utf-8"))
        except Exception as exc:
            raise ValueError("Failed to deserialize Kafka message") from exc

    @staticmethod
    def _log_message_metadata(msg: Message) -> None:
        log.info(
            "Consumed message topic=%s partition=%s offset=%s",
            msg.topic(),
            msg.partition(),
            msg.offset(),
        )

    def consume(
        self,
        handler: Callable[[dict], None],
        timeout: float = 1.0,
    ) -> None:
        log.info("Kafka consumer started")

        try:
            while self._running:
                msg = self._consumer.poll(timeout)

                if msg is None:
                    continue

                if msg.error():
                    log.error("Kafka consumer error: %s", msg.error())
                    continue

                try:
                    self._log_message_metadata(msg)

                    event = self._deserialize_message(msg)

                    handler(event)

                except Exception:
                    log.exception(
                        "Failed processing message topic=%s partition=%s offset=%s",
                        msg.topic(),
                        msg.partition(),
                        msg.offset(),
                    )

        except KafkaException:
            log.exception("Kafka consumer failure")

        finally:
            log.info("Closing Kafka consumer")
            self._consumer.close()
