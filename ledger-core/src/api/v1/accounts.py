from __future__ import annotations

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, field_validator

from api.dependencies import get_account_repo
from application.ports.account_repo import AccountRepo
from application.use_cases.list_accounts_by_owner import list_accounts_by_owner
from application.use_cases.get_account import get_account
from application.use_cases.create_account import create_account


class CreateAccountRequest(BaseModel):
    owner_id: uuid.UUID
    currency: str
    metadata: dict[str, str] = {}

    @field_validator("currency")
    @classmethod
    def currency_must_be_valid(cls, value: str) -> str:
        if len(value) != 3 or not value.isalpha():
            raise ValueError("Currency must be a 3-letter code")
        return value.upper()
    

class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    owner_id: uuid.UUID
    currency: str
    status: str
    created_at: datetime
    metadata: dict[str, str]


router = APIRouter(prefix="/v1/accounts", tags=["Accounts"])


@router.post(
    "/",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Account",
    description="Create a new account for a given owner and currency.",
)
async def create_account_route(
    body: CreateAccountRequest,
    repo: AccountRepo = Depends(get_account_repo),
) -> AccountResponse:
    account = await create_account(
        repo=repo,
        owner_id=body.owner_id,
        currency=body.currency,
        metadata=body.metadata,
    )
    return AccountResponse.model_validate(account)


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    summary="Get Account",
    description="Retrieve account details by account ID.",
)
async def get_account_route(
    account_id: uuid.UUID,
    repo: AccountRepo = Depends(get_account_repo),
) -> AccountResponse:
    account = await get_account(repo=repo, account_id=account_id)
    return AccountResponse.model_validate(account)
