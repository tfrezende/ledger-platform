import pytest
from unittest.mock import AsyncMock

from application.use_cases.create_account import CreateAccountCommand, create_account
from domain.account import AccountStatus


@pytest.mark.unit
async def test_create_account_returns_active_account() -> None:
    repo = AsyncMock()
    repo.save.return_value = None

    cmd = CreateAccountCommand(
        owner_id=__import__("uuid").uuid4(),
        currency="usd"
    )
    account = await create_account(repo, cmd)

    assert account.status == AccountStatus.ACTIVE
    assert account.currency == "USD"
    repo.save.assert_called_once_with(account)
    