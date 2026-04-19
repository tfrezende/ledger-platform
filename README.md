# ledger-platform

A production-grade, event-driven financial ledger system built as a polyglot monorepo. Designed to demonstrate distributed systems architecture, domain-driven design, and real-world engineering tradeoffs across multiple languages and runtimes.

---

## Architecture overview

```
api-gateway (separate repo — NestJS)
       │
       ▼
┌─────────────────────────────────────────────────┐
│               ledger-platform/                  │
│                                                 │
│  ledger-core          transaction-service       │
│  Python + FastAPI     Java + Spring Boot        │
│  accounts, balances   posting, validation       │
│  read-optimized       outbox, ACID              │
│                                                 │
│  event-relay          audit-service             │
│  Go                   Java + Spring Boot        │
│  outbox → Kafka       immutable event log       │
│                                                 │
│  notification-worker                            │
│  Python                                         │
│  Kafka consumer · email/push/SMS                │
└─────────────────────────────────────────────────┘
         │              │
         ▼              ▼
      Kafka          Postgres + Redis
```

Every state change produces an event. Services communicate asynchronously via Kafka topics. No service calls another directly at runtime.

---

## Services

| Service               | Language           | Responsibility                                       |
| --------------------- | ------------------ | ---------------------------------------------------- |
| `ledger-core`         | Python + FastAPI   | Accounts, entries, balance reads                     |
| `transaction-service` | Java + Spring Boot | Transaction posting, double-entry validation, outbox |
| `event-relay`         | Go                 | Polls outbox table, publishes to Kafka               |
| `audit-service`       | Java + Spring Boot | Immutable compliance event log                       |
| `notification-worker` | Python             | Consumes events, dispatches email/push/SMS           |

The [API gateway](https://github.com/tfrezende/api-gateway-saas) lives in a separate repository and handles authentication, rate limiting, and idempotency before routing to this system.

---

## Key design decisions

**Double-entry by design.** Every transaction posts two or more entries that sum to zero. Entries are immutable and append-only — no updates, no deletes. Balance is always derived from entries, never stored as mutable state.

**Transactional outbox.** The `transaction-service` writes events to an `outbox` table within the same database transaction that posts the ledger entries. The `event-relay` polls this table and publishes to Kafka, guaranteeing at-least-once delivery with no data loss.

**Money is never a float.** All monetary values are stored as integers in the smallest currency unit (e.g. cents). The `Money` value object carries both amount and currency explicitly.

**Polyglot by design.** Language choice follows domain requirements — Spring Boot for ACID-critical transaction logic, FastAPI for rapid query iteration, Go for the high-throughput relay worker.

---

## Repository structure

```
ledger-platform/
├── services/
│   ├── ledger-core/          # Python + FastAPI
│   ├── transaction-service/  # Java + Spring Boot
│   ├── event-relay/          # Go
│   ├── audit-service/        # Java + Spring Boot
│   └── notification-worker/  # Python
├── shared/
│   └── event-schemas/        # JSON Schema definitions for all Kafka events
├── infra/
│   ├── docker-compose.yml    # Full local stack
│   ├── k8s/                  # Kubernetes manifests
│   └── migrations/           # Cross-service DB migration notes
└── .github/
    └── workflows/            # Per-service CI pipelines (path-filtered)
```

---

## Running locally

**Prerequisites:** Docker, Docker Compose.

```bash
git clone https://github.com/tfrezende/ledger-platform
cd ledger-platform
docker compose -f infra/docker-compose.yml up
```

This starts Postgres, Redis, Kafka, and all services. The API is available via the gateway at `http://localhost:3000`.

Per-service development instructions (hot reload, test commands, env vars) are documented in each service's own `README.md`.

---

## Event topics

| Topic                    | Published by          | Consumed by                            |
| ------------------------ | --------------------- | -------------------------------------- |
| `transaction.created`    | `transaction-service` | `audit-service`, `notification-worker` |
| `transaction.reversed`   | `transaction-service` | `audit-service`, `notification-worker` |
| `balance.updated`        | `event-relay`         | `ledger-core` (cache invalidation)     |
| `account.status_changed` | `ledger-core`         | `audit-service`, `notification-worker` |

Event schemas are versioned and defined in `shared/event-schemas/`.

---

## Status

Active development. Services are being built in this order:

- [x] Architecture design
- [ ] `ledger-core` — in progress
- [ ] `transaction-service`
- [ ] `event-relay`
- [ ] `audit-service`
- [ ] `notification-worker`
- [ ] Frontend (planned)
