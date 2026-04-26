from __future__ import annotations

from uuid import UUID

from application.ports.account_repo import AccountRepo
from domain.account import Account


async def list_accounts_by_owner(repo: AccountRepo, owner_id: UUID) -> list[Account]:
    return await repo.list_by_owner(owner_id)