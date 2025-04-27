import pytest
from httpx import AsyncClient
from faker import Faker
from tests.v1.modules.get_access_token import get_access_token

pytestmark = pytest.mark.asyncio
fake = Faker()


async def test_get_me_authenticated(client: AsyncClient):
    access_token, email = await get_access_token(client)

    response = await client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == email


async def test_get_me_unauthenticated(client: AsyncClient):
    response = await client.get("/users/me")
    assert response.status_code == 401
    assert "detail" in response.json()
