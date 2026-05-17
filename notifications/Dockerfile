FROM python:3.12-slim

# Install uv
RUN pip install uv

# Working directory
WORKDIR /app

# Copy BOTH projects
COPY kafka_lib /app/kafka_lib
COPY notifications /app/notifications

# Move into service directory
WORKDIR /app/notifications

# Install dependencies
RUN uv sync --frozen

# Run service
CMD ["uv", "run", "python", "-m", "notifications.core"]