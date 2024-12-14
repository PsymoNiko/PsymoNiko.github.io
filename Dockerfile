FROM python:3.12-slim-bookworm as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy dependencies file first (leverage caching)
COPY develop.txt /app/
#RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r develop.txt
RUN pip install --no-cache-dir -r develop.txt
#RUN pip install -r develop.txt

# Final runtime image
FROM python:3.12-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy dependencies and app files
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . /app/

# Expose application port
EXPOSE 8000

CMD ["sh", "/app/migrate_run.sh"]

