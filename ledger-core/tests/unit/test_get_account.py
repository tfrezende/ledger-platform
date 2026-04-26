from __future__ import annotations

import pytest
from unittest.mock import AsyncMock

from application.use_cases.get_account import get_account
from domain.exceptions import AccountNotFoundError


@pytest.mark.unit
async def test_get_account_returns_account(sample_account) -> None:
    repo = AsyncMock()
    repo.get.return_value = sample_account

    account = await get_account(repo, sample_account.id)

    assert account == sample_account
    repo.get.assert_called_once_with(sample_account.id)


@pytest.mark.unit
async def test_get_account_raises_not_found() -> None:
    repo = AsyncMock()
    repo.get.side_effect = AccountNotFoundError("missing-id")

    with pytest.raises(AccountNotFoundError):
        await get_account(repo, __import__("uuid").uuid4())