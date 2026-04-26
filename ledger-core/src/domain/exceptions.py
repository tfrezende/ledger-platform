class LedgerError(Exception):
    """Base class for all exceptions raised by the ledger."""


class AccountNotFoundError(LedgerError):
    """Raised when an account is not found."""
    def __init__(self, account_id: object) -> None:
        super().__init__(f"Account with ID '{account_id}' not found.")


class AccountFrozenError(LedgerError):
    """Raised when an operation is attempted on a frozen account."""
    def __init__(self, account_id: object) -> None:
        super().__init__(f"Account with ID '{account_id}' is frozen.")


class AccountClosedError(LedgerError):
    """Raised when an operation is attempted on a closed account."""
    def __init__(self, account_id: object) -> None:
        super().__init__(f"Account with ID '{account_id}' is closed.")