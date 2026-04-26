from __future__ import annotations

import uuid
from typing import Protocol

from domain.account import Account


class AccountRepo(Protocol):
    async def get(self, account_id: uuid.UUID) -> Account:
        ...
    async def save(self, account: Account) -> None:
        ...
    async def list_by_owner(self, owner_id: uuid.UUID) -> list[Account]:
        ...
