from httpx import AsyncClient
from fastapi import status
from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode


async def test_get_me_authenticated(auth_client: AsyncClient):
    response = await auth_client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["email"] != ""
    assert response.json()["id"] != ""
    assert "wallet" in response.json()
    assert response.json()["wallet"]["balance"] == 0


async def test_get_me_unauthenticated(client: AsyncClient):
    response = await client.get("/users/me")
    check_api_exception_response(
        response,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail_code=ErrorCode.UNAUTHORIZED,
    )
