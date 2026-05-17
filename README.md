# InventoryLens

InventoryLens is a real-time inventory intelligence and observability platform that simulates an e-commerce system where customer orders continuously impact inventory levels, enabling real-time alerts and comprehensive observability dashboards.

## Architecture & Services

This project is composed of several services, orchestrated via Docker Compose:

- **app**: FastAPI service for inventory management and product APIs. Handles inventory updates and publishes events to Kafka.
- **notifications**: Listens to inventory events from Kafka and sends low-stock email alerts via SMTP (Maildev).
- **kafka_lib**: Shared Python library for Kafka producer/consumer logic, used by all services.
- **str**: (Optional) Sale simulator that generates order events to test the system.
- **postgres**: Database for inventory and product data.
- **kafka**: Kafka broker for event streaming.
- **maildev**: SMTP server and web UI for testing email notifications.

## Quick Start

1. **Clone the repository:**
	```sh
	git clone <repo-url>
	cd inventory-lens
	```

2. **Start all services:**
	```sh
	./start.sh
	```
	This will build and launch all containers (API, notifications, Kafka, Postgres, Maildev, etc).

3. **Access the services:**
	- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
	- Maildev UI: [http://localhost:1080](http://localhost:1080)

## Development Setup

Each service is a standalone Python project (with its own `pyproject.toml`). For local development:

1. Create a virtual environment in the service directory (e.g. `app/`, `notifications/`, `str/`).
2. Run `uv sync` or `pip install -r requirements.txt` as appropriate.
3. Use the shared `kafka_lib` via local path dependency (see `[tool.uv.sources]` in each service's `pyproject.toml`).

## Environment Variables

Key environment variables (see `docker-compose.yaml`):

- `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker address (usually `kafka:9092` in Docker)
- `DB_URI`: Postgres connection string (e.g. `postgresql+psycopg2://postgres:postgres@postgres:5432/ilens-db`)
- `TOPIC`: Kafka topic for inventory events
- `GROUP_ID`: Kafka consumer group (for notifications, str, etc)
- `SMTP_HOST`, `SMTP_PORT`, `FROM_EMAIL`: For notifications service

## Useful Commands

- Start all services: `./start.sh`
- Stop all services: `docker-compose down -v`
- View logs: `docker-compose logs -f`
- Rebuild everything: `docker-compose build --no-cache`
- Run STR: `cd str && uv run main.py`

## Project Structure

- `app/` - FastAPI inventory and product API
- `notifications/` - Email alert service
- `kafka_lib/` - Shared Kafka code
- `str/` - Sale simulator (optional)
- `db/` - Database initialization scripts
- `docker-compose.yaml` - Orchestration for all services

# TODO: 
Validate requests for Kafka