import pytest
from httpx import AsyncClient
from tests.v1.common.unauthorized_response import check_unauthorized_response

async def test_get_me_authenticated(client: AsyncClient, access_token):
    response = await client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] != ""
    assert response.json()["id"] != ""

async def test_get_me_unauthenticated(client: AsyncClient):
    response = await client.get("/users/me")
    check_unauthorized_response(response)
