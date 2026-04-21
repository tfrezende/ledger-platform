# --- builder stage ---
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency manifests first (layer cache)
COPY pyproject.toml uv.lock ./

# Install runtime deps only into /app/.venv
RUN uv sync --frozen --no-dev --no-install-project

# --- runtime stage ---
FROM python:3.12-slim AS runtime

WORKDIR /app

# Non-root user
RUN addgroup --system ledger && adduser --system --ingroup ledger ledger

# Copy the venv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application source
COPY src/ ./src/

# Ensure the venv is used
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER ledger

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
