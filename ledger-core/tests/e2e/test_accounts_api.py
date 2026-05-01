import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.e2e
async def test_create_account_returns_201(client: AsyncClient) -> None:
    response = await client.post(
        "/v1/accounts/",
        json={"owner_id": str(uuid.uuid4()), "currency": "USD"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["currency"] == "USD"
    assert body["status"] == "active"
    assert "id" in body


@pytest.mark.e2e
async def test_create_account_invalid_currency_returns_422(client: AsyncClient) -> None:
    response = await client.post(
        "/v1/accounts/",
        json={"owner_id": str(uuid.uuid4()), "currency": "INVALID"},
    )

    assert response.status_code == 422


@pytest.mark.e2e
async def test_get_account_returns_200(client: AsyncClient) -> None:
    owner_id = str(uuid.uuid4())
    created = await client.post(
        "/v1/accounts/", json={"owner_id": owner_id, "currency": "EUR"}
    )
    account_id = created.json()["id"]

    response = await client.get(f"/v1/accounts/{account_id}")

    assert response.status_code == 200
    assert response.json()["id"] == account_id


@pytest.mark.e2e
async def test_get_account_not_found_returns_404(client: AsyncClient) -> None:
    response = await client.get(f"/v1/accounts/{uuid.uuid4()}")

    assert response.status_code == 404
    assert response.json()["error"] == "account_not_found"


@pytest.mark.e2e
async def test_list_owner_accounts_returns_all(client: AsyncClient) -> None:
    owner_id = str(uuid.uuid4())
    await client.post("/v1/accounts/", json={"owner_id": owner_id, "currency": "USD"})
    await client.post("/v1/accounts/", json={"owner_id": owner_id, "currency": "EUR"})

    response = await client.get(f"/v1/owners/{owner_id}/accounts")

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.e2e
async def test_list_owner_accounts_empty(client: AsyncClient) -> None:
    response = await client.get(f"/v1/owners/{uuid.uuid4()}/accounts")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.e2e
async def test_health_live(client: AsyncClient) -> None:
    response = await client.get("/health/live")

    assert response.status_code == 200


@pytest.mark.e2e
async def test_health_ready(client: AsyncClient) -> None:
    response = await client.get("/health/ready")

    assert response.status_code == 200