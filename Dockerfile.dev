#FROM python:3.10-alpine AS builder
FROM python:3.12-slim-bookworm as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Install system dependencies for building wheels and psycopg2
#RUN apt-get update && apt-get install -y \
#    build-essential \
#    libpq-dev \
#    libffi-dev \
#    libssl-dev \
#    --no-install-recommends \
#    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /code

# Install Python dependencies
COPY requirements.txt /code
#RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install -r requirements.txt
# Use a final runtime image
#FROM python:3.10-alpine
FROM python:3.12-slim-bookworm
# Install system runtime dependencies
RUN apt-get update && apt-get install -y libpq-dev --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables again for runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Copy only necessary files to minimize the image size
#COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .

# Expose the port that Daphne or Gunicorn will bind to
EXPOSE 8000
CMD ["sh", "/code/migrate_run.sh"]
#CMD ["gunicorn", "-b", "0.0.0.0:8000", "core.wsgi:application"]
# Entry point for Gunicorn with ASGI support
#CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "core.asgi:application", "--workers", "3"]
