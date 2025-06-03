import pytest

from httpx import AsyncClient
from tests.common.check_error_response import check_unauthorized_response


@pytest.mark.asyncio
async def test_verify_user_api_key_success(client: AsyncClient, user, user_api_key):
    resp = await client.post(
        "/user-api-keys/verify",
        headers={"X-API-KEY": user_api_key.api_key},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("is_valid") is True


@pytest.mark.asyncio
async def test_verify_has_expires_at_user_api_key_success(
    client: AsyncClient, user, user_api_key_with_expires_at
):
    resp = await client.post(
        "/user-api-keys/verify",
        headers={"X-API-KEY": user_api_key_with_expires_at.api_key},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("is_valid") is True


@pytest.mark.asyncio
async def test_verify_expired_user_api_key(
    client: AsyncClient, user, expired_user_api_key
):
    """An expired API key should be rejected with 401."""
    resp = await client.post(
        "/user-api-keys/verify",
        headers={"X-API-KEY": expired_user_api_key.api_key},
    )
    check_unauthorized_response(resp, code="expired_api_key")


@pytest.mark.asyncio
async def test_verify_user_api_key_missing_header(client: AsyncClient):
    """Requests without the X‑API‑KEY header should be rejected with 401."""
    resp = await client.post("/user-api-keys/verify")
    check_unauthorized_response(resp)


@pytest.mark.asyncio
async def test_verify_user_api_key_invalid(client: AsyncClient):
    """An invalid / unknown API‑Key should be rejected with 401."""
    resp = await client.post(
        "/user-api-keys/verify",
        headers={"X-API-KEY": "invalid123"},
    )
    check_unauthorized_response(resp, code="invalid_api_key")


@pytest.mark.asyncio
async def test_verify_user_api_key_success_without_api_key(
    auth_client: AsyncClient, user, user_api_key
):
    resp = await auth_client.post(
        "/user-api-keys/verify",
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("is_valid") is True
