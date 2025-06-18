from httpx import AsyncClient
from fastapi import status
from tests.common.check_error_response import check_api_exception_response


async def test_jwt_logout_success(client: AsyncClient, access_token):
    response = await client.post(
        "/auth/jwt/logout", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 204

    me = await client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert me.status_code == 200


async def test_jwt_logout_unauthorized(client: AsyncClient):
    response = await client.post("/auth/jwt/logout")

    assert response.status_code == 401
    check_api_exception_response(
        response,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail_code="unauthorized",
    )
