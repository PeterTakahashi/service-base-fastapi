from httpx import AsyncClient
from tests.v1.common.unauthorized_response import check_unauthorized_response


async def test_get_me_authenticated(auth_client: AsyncClient):
    response = await auth_client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["email"] != ""
    assert response.json()["id"] != ""


async def test_get_me_unauthenticated(client: AsyncClient):
    response = await client.get("/users/me")
    check_unauthorized_response(response)
