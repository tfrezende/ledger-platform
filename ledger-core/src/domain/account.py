from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum


class AccountStatus(StrEnum):
    ACTIVE = "active"
    CLOSED = "closed"
    FROZEN = "frozen"


@dataclass(frozen=True)
class Account:
    id: uuid.UUID
    owwner_id: uuid.UUID
    currency: str
    status: AccountStatus
    created_at: datetime
    metadata: dict[str, str] = field(default_factory=dict)
