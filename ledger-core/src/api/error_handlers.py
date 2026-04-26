from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.exceptions import (
    AccountNotFoundError,
    AccountClosedError,
    AccountFrozenError,
    LedgerError,
)


def _error_response(status_code: int, error: str, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": error, "detail": detail},
    )


async def account_not_found_handler(_request: Request, exc: AccountNotFoundError) -> JSONResponse:
    return _error_response(404, "account_not_found", str(exc))


async def account_closed_handler(_request: Request, exc: AccountClosedError) -> JSONResponse:
    return _error_response(422, "account_closed", str(exc))


async def account_frozen_handler(_request: Request, exc: AccountFrozenError) -> JSONResponse:
    return _error_response(422, "account_frozen", str(exc))


async def unhandled_ledger_error_handler(_request: Request, _exc: LedgerError) -> JSONResponse:
    return _error_response(500, "internal_error", "An unexpected error occurred")


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AccountNotFoundError, account_not_found_handler)
    app.add_exception_handler(AccountClosedError, account_closed_handler)
    app.add_exception_handler(AccountFrozenError, account_frozen_handler)
    app.add_exception_handler(LedgerError, unhandled_ledger_error_handler)
    