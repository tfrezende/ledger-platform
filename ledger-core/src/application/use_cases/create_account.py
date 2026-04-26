from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from application.ports.account_repo import AccountRepo
from domain.account import Account, AccountStatus


@dataclass
class CreateAccountCommand:
    owner_id: uuid.UUID
    currency: str
    metadata: dict[str, str] = field(default_factory=dict)


async def create_account(repo: AccountRepo, cmd: CreateAccountCommand) -> Account:
    account = Account(
        id=uuid.uuid4(),
        owner_id=cmd.owner_id,
        currency=cmd.currency.upper(),
        status=AccountStatus.ACTIVE,
        created_at=datetime.now(timezone.utc),
        metadata=cmd.metadata,
    )
    await repo.save(account)
    return account