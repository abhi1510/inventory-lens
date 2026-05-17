FROM python:3.12-slim

# Install uv
RUN pip install uv

# Working directory
WORKDIR /app

# Copy libs
COPY kafka_lib /app/kafka_lib
COPY app /app/app

# Move into service directory
WORKDIR /app/app

# Install dependencies
RUN uv sync --frozen

# Run service
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]