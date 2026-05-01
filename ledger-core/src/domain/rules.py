from domain.account import Account, AccountStatus
from domain.exceptions import AccountClosedError, AccountFrozenError


def assert_account_active(account: Account) -> None:
    if account.status == AccountStatus.FROZEN:
        raise AccountFrozenError(account.id)
    if account.status == AccountStatus.CLOSED:
        raise AccountClosedError(account.id)