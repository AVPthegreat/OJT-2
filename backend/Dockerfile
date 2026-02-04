# Backend Dockerfile
# Multi-stage build for development and production

# ============================================
# Base stage - common dependencies
# ============================================
FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# ============================================
# Development stage
# ============================================
FROM base as development

# Install all dependencies including dev tools
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir watchfiles debugpy

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBUG=true

# Mount point for live code reload
WORKDIR /app

# Expose ports (8000 for app, 5678 for debugger)
EXPOSE 8000 5678

# Development command with hot reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app"]

# ============================================
# Production stage
# ============================================
FROM base as production

# Install production dependencies only
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Set production environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBUG=false

EXPOSE 8000

# Production command with multiple workers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
