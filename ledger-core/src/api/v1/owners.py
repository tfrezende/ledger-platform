from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends

from api.dependencies import get_account_repo
from api.v1.accounts import AccountResponse
from application.ports.account_repo import AccountRepo
from application.use_cases.list_accounts_by_owner import list_accounts_by_owner

router = APIRouter(prefix="/v1/owners", tags=["Owners"])


@router.get(
    "/{owner_id}/accounts",
    response_model=list[AccountResponse],
    summary="List Accounts by Owner",
    description="Retrieve a list of accounts associated with a specific owner ID.",
)
async def list_owner_accounts_route(
    owner_id: uuid.UUID,
    repo: AccountRepo = Depends(get_account_repo),
) -> list[AccountResponse]:
    accounts = await list_accounts_by_owner(repo=repo, owner_id=owner_id)
    return [AccountResponse.model_validate(account) for account in accounts]
