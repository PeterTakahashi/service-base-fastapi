import pytest
from httpx import AsyncClient
from faker import Faker
from tests.v1.modules.get_access_token import get_access_token

pytestmark = pytest.mark.asyncio
fake = Faker()

async def test_update_me_email(client: AsyncClient):
    access_token, old_email = await get_access_token(client)
    new_email = fake.unique.email()

    response = await client.patch(
        "/users/me",
        json={"email": new_email},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == new_email
    assert response.json()["email"] != old_email

async def test_update_me_unauthenticated(client: AsyncClient):
    response = await client.patch("/users/me", json={"email": fake.unique.email()})
    assert response.status_code == 401
