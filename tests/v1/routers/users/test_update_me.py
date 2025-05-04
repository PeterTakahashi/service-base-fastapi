"""Tests for updating the authenticated user's information."""

from httpx import AsyncClient
from tests.v1.common.unauthorized_response import check_unauthorized_response


async def test_update_me_email(auth_client: AsyncClient, faker):
    """Test updating the email of the authenticated user."""
    new_email = faker.unique.email()

    response = await auth_client.patch(
        "/users/me",
        json={"email": new_email},
    )

    assert response.status_code == 200
    assert response.json()["email"] == new_email


async def test_update_me_unauthenticated(client: AsyncClient):
    """Test updating user information without authentication."""
    response = await client.patch("/users/me", json={"email": "test@test.com"})
    check_unauthorized_response(response)


async def test_update_me_invalid_email(auth_client: AsyncClient):
    """Test updating the email with an invalid email format."""
    invalid_email = "invalid-email"

    response = await auth_client.patch(
        "/users/me",
        json={"email": invalid_email},
    )

    assert response.status_code == 422
    assert response.json()["errors"][0]["detail"].startswith(
        "value is not a valid email address"
    )


async def test_update_me_no_changes(auth_client: AsyncClient):
    """Test updating user information with no changes."""
    response = await auth_client.patch("/users/me", json={})

    assert response.status_code == 200

async def test_update_me_multiple_fields(auth_client: AsyncClient, faker):
    """Test updating multiple fields of the authenticated user."""
    new_email = faker.unique.email()

    response = await auth_client.patch(
        "/users/me",
        json={"email": new_email, "password": "newpassword"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == new_email
