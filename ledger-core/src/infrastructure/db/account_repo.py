from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.account import Account, AccountStatus
from domain.exceptions import AccountNotFoundError
from infrastructure.db.models import AccountModel


def _to_domain(model: AccountModel) -> Account:
    return Account(
        id=model.id,
        owner_id=model.owner_id,
        currency=model.currency,
        status=AccountStatus(model.status),
        created_at=model.created_at,
        metadata=model.metadata_ or {},
    )


def _to_model(account: Account) -> AccountModel:
    model = AccountModel()
    model.id = account.id
    model.owner_id = account.owner_id
    model.currency = account.currency
    model.status = account.status.value
    model.created_at = account.created_at
    model.metadata_ = account.metadata
    return model


class SqlAccountRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, account_id: uuid.UUID) -> Account:
        model = await self._session.get(AccountModel, account_id)
        if model is None:
            raise AccountNotFoundError(account_id)
        return _to_domain(model)

    async def save(self, account: Account) -> None:
        model = _to_model(account)
        await self._session.merge(model)

    async def list_by_owner(self, owner_id: uuid.UUID) -> list[Account]:
        result = await self._session.execute(
            select(AccountModel).where(AccountModel.owner_id == owner_id)
        )
        return [_to_domain(row) for row in result.scalars()]