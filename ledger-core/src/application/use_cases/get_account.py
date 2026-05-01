from uuid import UUID

from application.ports.account_repo import AccountRepo
from domain.account import Account


async def get_account(repo: AccountRepo, account_id: UUID) -> Account:
    return await repo.get(account_id)
