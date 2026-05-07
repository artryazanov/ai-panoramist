FROM python:3.12-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set python path
ENV PYTHONPATH=/app

# Create output directory
RUN mkdir -p /app/output

# Default command (can be overridden in docker-compose)
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
