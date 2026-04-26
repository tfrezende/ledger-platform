from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

from domain.account import Account, AccountStatus
from domain.exceptions import AccountNotFoundError
from infrastructure.db.account_repo import SqlAccountRepo


def make_account(owner_id: uuid.UUID | None = None) -> Account:
    return Account(
        id=uuid.uuid4(),
        owner_id=owner_id or uuid.uuid4(),
        currency="USD",
        status=AccountStatus.ACTIVE,
        created_at=datetime.now(timezone.utc),
    )


@pytest.mark.integration
async def test_save_and_get_account(session) -> None:
    repo = SqlAccountRepo(session)
    account = make_account()

    await repo.save(account)
    retrieved = await repo.get(account.id)

    assert retrieved.id == account.id
    assert retrieved.currency == account.currency
    assert retrieved.status == account.status


@pytest.mark.integration
async def test_get_raises_not_found(session) -> None:
    repo = SqlAccountRepo(session)

    with pytest.raises(AccountNotFoundError):
        await repo.get(uuid.uuid4())


@pytest.mark.integration
async def test_list_by_owner_returns_all_account(session) -> None:
    repo = SqlAccountRepo(session)
    owner_id = uuid.uuid4()
    
    account_a = make_account(owner_id=owner_id)
    account_b = make_account(owner_id=owner_id)
    await repo.save(account_a)
    await repo.save(account_b)

    results = await repo.list_by_owner(owner_id)

    assert len(results) == 2
    assert {result.id for result in results} == {account_a.id, account_b.id}


@pytest.mark.integration
async def test_list_by_owner_returns_empty(session) -> None:
    repo = SqlAccountRepo(session)

    results = await repo.list_by_owner(uuid.uuid4())

    assert len(results) == 0


@pytest.mark.integration
async def test_save_is_idempotent(session) -> None:
    repo = SqlAccountRepo(session)
    account = make_account()

    await repo.save(account)
    updated = Account(
        id=account.id,
        owner_id=account.owner_id,
        currency="EUR",
        status=AccountStatus.FROZEN,
        created_at=account.created_at,
    )

    await repo.save(updated)

    retrieved = await repo.get(account.id)
    assert retrieved.status == AccountStatus.FROZEN
