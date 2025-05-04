from httpx import AsyncClient
from tests.common.check_error_response import check_unauthorized_response


async def test_update_me_email(auth_client: AsyncClient, faker):
    new_email = faker.unique.email()

    response = await auth_client.patch(
        "/users/me",
        json={"email": new_email},
    )

    assert response.status_code == 200
    assert response.json()["email"] == new_email


async def test_update_me_unauthenticated(client: AsyncClient):
    response = await client.patch("/users/me", json={"email": "test@test.com"})
    check_unauthorized_response(response)
