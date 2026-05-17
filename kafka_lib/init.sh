#!/bin/bash

set -e

echo "Using broker: $KAFKA_BOOTSTRAP_SERVERS"

echo "⏳ Waiting for Kafka..."

for i in {1..30}; do
  kafka-topics --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" --list && break
  echo "Kafka not ready yet... retry $i"
  sleep 2
done

echo "🚀 Creating topics..."

kafka-topics --bootstrap-server "$KAFKA_BOOTSTRAP_SERVERS" \
  --create --if-not-exists \
  --topic inventory-events --partitions 3 --replication-factor 1

echo "✅ Topics created successfully"