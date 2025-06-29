import pytest

from httpx import AsyncClient
from fastapi import status
from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode


@pytest.mark.asyncio
async def test_verify_user_api_key_success(client: AsyncClient, user_api_key):
    resp = await client.post(
        "/api-keys/verify",
        headers={"X-API-KEY": user_api_key.api_key},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("is_valid") is True


@pytest.mark.asyncio
async def test_verify_has_expires_at_user_api_key_success(
    client: AsyncClient, user_api_key_with_expires_at
):
    resp = await client.post(
        "/api-keys/verify",
        headers={
            "X-API-KEY": user_api_key_with_expires_at.api_key,
            "Authorization": "",
        },
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
        "/api-keys/verify",
        headers={"X-API-KEY": expired_user_api_key.api_key, "Authorization": ""},
    )
    check_api_exception_response(
        resp,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail_code=ErrorCode.EXPIRED_API_KEY,
    )


@pytest.mark.asyncio
async def test_verify_user_api_key_null_string_header(client: AsyncClient):
    """Requests without the X‑API‑KEY header should be rejected with 401."""
    resp = await client.post("/api-keys/verify", headers={"X-API-KEY": ""})
    check_api_exception_response(
        resp,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail_code=ErrorCode.UNAUTHORIZED_API_KEY,
    )


@pytest.mark.asyncio
async def test_verify_user_api_key_blank_header(client: AsyncClient):
    """Requests without the X‑API‑KEY header should be rejected with 401."""
    resp = await client.post("/api-keys/verify")
    assert resp.json() == {
        "type": "about:blank",
        "title": "Unprocessable Entity",
        "status": 422,
        "instance": "http://test/app/v1/api-keys/verify",
        "errors": [
            {
                "status": "422",
                "code": "validation_error",
                "title": "Validation Error",
                "detail": "Field required",
                "source": {"pointer": "#/header/X-API-KEY"},
            },
            {
                "status": "422",
                "code": "validation_error",
                "title": "Validation Error",
                "detail": "Field required",
                "source": {"pointer": "#/header/X-API-KEY"},
            },
        ],
    }


@pytest.mark.asyncio
async def test_verify_user_api_key_missing_header(client: AsyncClient):
    """Requests without the X‑API‑KEY header should be rejected with 401."""
    resp = await client.post(
        "/api-keys/verify", headers={"X-API-KEY": "user_test_api_key_123"}
    )
    check_api_exception_response(
        resp,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail_code=ErrorCode.UNAUTHORIZED_API_KEY,
    )


# ---------------------------------------------------------------------------
# New tests for IP / Origin allow‑list logic
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_verify_user_api_key_allowed_origin_success(
    client: AsyncClient,
    user,
    user_api_key_factory,
):
    """When allowed_origin matches the request Origin header, verification succeeds."""
    api_key = await user_api_key_factory.create(
        user=user,
        allowed_origin="https://example.com",
        allowed_ip="127.0.0.1",
    )
    resp = await client.post(
        "/api-keys/verify",
        headers={
            "X-API-KEY": api_key.api_key,
            "Origin": "https://example.com",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["is_valid"] is True


@pytest.mark.asyncio
async def test_verify_user_api_key_invalid_origin(
    client: AsyncClient,
    user,
    user_api_key_factory,
):
    """A mismatching Origin header should be rejected with 401/invalid_origin."""
    api_key = await user_api_key_factory.create(
        user=user,
        allowed_origin="https://example.com",
        allowed_ip="127.0.0.1",
    )
    resp = await client.post(
        "/api-keys/verify",
        headers={
            "X-API-KEY": api_key.api_key,
            "Origin": "https://evil.com",
            "Authorization": "",
        },
    )
    check_api_exception_response(
        resp,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail_code=ErrorCode.INVALID_ORIGIN,
    )


@pytest.mark.asyncio
async def test_verify_user_api_key_allowed_ip_success(
    client: AsyncClient,
    user,
    user_api_key_factory,
):
    """When allowed_ip matches the client IP (127.0.0.1 in tests), verification succeeds."""
    api_key = await user_api_key_factory.create(
        user=user,
        allowed_ip="127.0.0.1",
        allowed_origin=None,
    )
    resp = await client.post(
        "/api-keys/verify",
        headers={"X-API-KEY": api_key.api_key, "Authorization": ""},
    )
    assert resp.status_code == 200
    assert resp.json()["is_valid"] is True


@pytest.mark.asyncio
async def test_verify_user_api_key_invalid_ip(
    client: AsyncClient,
    user,
    user_api_key_factory,
):
    """A mismatching client IP should be rejected with 401/invalid_ip."""
    api_key = await user_api_key_factory.create(
        user=user,
        allowed_ip="10.0.0.1",
    )
    resp = await client.post(
        "/api-keys/verify",
        headers={"X-API-KEY": api_key.api_key, "Authorization": ""},
    )
    check_api_exception_response(
        resp, status_code=status.HTTP_401_UNAUTHORIZED, detail_code=ErrorCode.INVALID_IP
    )


@pytest.mark.asyncio
async def test_verify_user_api_key_allowed_ip_and_origin_success(
    client: AsyncClient,
    user,
    user_api_key_factory,
):
    """Both IP and Origin match => verification succeeds."""
    api_key = await user_api_key_factory.create(
        user=user,
        allowed_ip="127.0.0.1",
        allowed_origin="https://example.com",
    )
    resp = await client.post(
        "/api-keys/verify",
        headers={
            "X-API-KEY": api_key.api_key,
            "Origin": "https://example.com",
        },
    )
    assert resp.status_code == 200
    assert resp.json()["is_valid"] is True
