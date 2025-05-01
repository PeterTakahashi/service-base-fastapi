from httpx import AsyncClient
from tests.v1.common.unauthorized_response import check_unauthorized_response

async def test_update_me_email(client: AsyncClient, access_token, faker):
    new_email = faker.unique.email()

    response = await client.patch(
        "/users/me",
        json={"email": new_email},
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == new_email

async def test_update_me_unauthenticated(client: AsyncClient):
    response = await client.patch("/users/me", json={"email": "test@test.com"})
    check_unauthorized_response(response)
