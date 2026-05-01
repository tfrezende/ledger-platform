import uuid

import pytest
from unittest.mock import AsyncMock

from application.use_cases.list_accounts_by_owner import list_accounts_by_owner


@pytest.mark.unit
async def test_list_accounts_by_owner_returns_accounts(sample_account) -> None:
    repo = AsyncMock()
    repo.list_by_owner.return_value = [sample_account]

    accounts = await list_accounts_by_owner(repo, sample_account.owner_id)

    assert accounts == [sample_account]
    repo.list_by_owner.assert_called_once_with(sample_account.owner_id)


@pytest.mark.unit
async def test_list_accounts_by_owner_returns_empty_list() -> None:
    repo = AsyncMock()
    repo.list_by_owner.return_value = []

    accounts = await list_accounts_by_owner(repo, uuid.uuid4())

    assert accounts == []