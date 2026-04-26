# ledger-core

Read-optimized financial ledger service. Part of [ledger-platform](../README.md).

Manages accounts and their metadata, stores immutable double-entry ledger entries, and serves balance queries and paginated entry history. It does **not** post transactions — entries are written by `transaction-service` directly to the shared database and exposed here via a read API.

## Architecture

Hexagonal (ports & adapters) with a strict inward dependency rule:

```
api/          → application/   → domain/
infrastructure/ → application/ → domain/
```

- **`domain/`** — pure Python dataclasses, value objects, domain exceptions, and double-entry invariants. No framework imports.
- **`application/`** — async use cases and `ports/` Protocol interfaces. Depends only on the domain, never on infrastructure.
- **`infrastructure/`** — SQLAlchemy ORM models, async Postgres session factory, Redis cache adapter, Alembic migrations.
- **`api/`** — FastAPI routers under `v1/`, Pydantic schemas, dependency injection wiring, error handlers.

## Stack

| Concern    | Technology             |
| ---------- | ---------------------- |
| Framework  | FastAPI                |
| ORM        | SQLAlchemy 2.0 (async) |
| Database   | PostgreSQL 16          |
| Cache      | Redis 7                |
| Migrations | Alembic                |
| Validation | Pydantic v2            |
| Runtime    | Python 3.12, uvicorn   |
| Tests      | pytest, testcontainers |

## Getting started

**Prerequisites:** [uv](https://docs.astral.sh/uv/), Docker

```bash
# Install dependencies
uv sync --group dev

# Copy and configure environment
cp .env.example .env

# Start Postgres + Redis
docker compose up postgres redis

# Run the app locally
uv run uvicorn main:app --reload --app-dir src
```

The API is available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Run with Docker

```bash
docker compose up --build
```

### Database migrations

```bash
# Apply all migrations
uv run alembic upgrade head

# Generate a new migration after changing ORM models
uv run alembic revision --autogenerate -m "description"
```

### Tests

```bash
uv run pytest -m unit             # unit tests only (no I/O)
uv run pytest -m integration      # requires running Postgres + Redis
uv run pytest -m e2e              # full stack
```

## API

### Accounts

| Method | Endpoint                         | Description                    |
| ------ | -------------------------------- | ------------------------------ |
| `POST` | `/v1/accounts/`                  | Create a new account           |
| `GET`  | `/v1/accounts/{account_id}`      | Get account by ID              |
| `GET`  | `/v1/owners/{owner_id}/accounts` | List all accounts for an owner |

Accounts have a `status` of `active`, `frozen`, or `closed`. Operations that mutate a non-active account return `422`.

## Health

| Endpoint            | Description                                  |
| ------------------- | -------------------------------------------- |
| `GET /health/live`  | Liveness — always 200 if the process is up   |
| `GET /health/ready` | Readiness — checks DB and Redis connectivity |

## Project status

| Feature                                    | Status      |
| ------------------------------------------ | ----------- |
| Feature 0 — Scaffold                       | ✅ Complete |
| Feature 1 — Account Management             | ✅ Complete |
| Feature 2 — Ledger Entries                 | 🔜 Planned  |
| Feature 3 — Balance Query                  | ⏳ Planned  |
| Feature 4 — Error Handling & Observability | ⏳ Planned  |
| Feature 5 — Test Pyramid & CI Hardening    | ⏳ Planned  |
