from httpx import AsyncClient
from tests.common.check_error_response import (
    check_api_exception_response,
)
from fastapi import status
from app.lib.error_code import ErrorCode


async def test_update_me_email(auth_client: AsyncClient, faker):
    new_email = faker.unique.email()

    response = await auth_client.patch(
        "/users/me",
        json={"email": new_email},
    )

    assert response.status_code == 200
    assert response.json()["email"] == new_email


async def test_update_me_password(auth_client: AsyncClient, faker, fake_email):
    new_password = faker.password()

    response = await auth_client.patch(
        "/users/me",
        json={"password": new_password},
    )

    assert response.status_code == 200
    assert response.json()["email"] == fake_email

    # Re-authenticate with the new password
    login_response = await auth_client.post(
        "/auth/jwt/login",
        headers={},
        data={
            "username": fake_email,
            "password": new_password,
        },
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


async def test_update_me_email_already_exists(
    client: AsyncClient, auth_client: AsyncClient, faker
):
    # 1. create a user
    email = faker.unique.email()
    password = faker.password(length=12)
    await client.post(
        "/auth/register/register", json={"email": email, "password": password}
    )

    # 2. update the email
    response = await auth_client.patch(
        "/users/me",
        json={"email": email},
    )
    # 3. check the response
    check_api_exception_response(
        response,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail_code=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        pointer="email",
    )


async def test_update_me_address(
    auth_client: AsyncClient, fake_address, other_fake_address
):
    response = await auth_client.patch(
        "/users/me",
        json={"address": fake_address.model_dump()},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["address"] is not None
    assert response_data["address"]["city"] == fake_address.city
    assert response_data["address"]["country"] == fake_address.country
    assert response_data["address"]["postal_code"] == fake_address.postal_code
    assert response_data["address"]["state"] == fake_address.state

    # second time
    response = await auth_client.patch(
        "/users/me",
        json={"address": other_fake_address.model_dump()},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["address"] is not None
    assert response_data["address"]["city"] == other_fake_address.city
    assert response_data["address"]["country"] == other_fake_address.country
    assert response_data["address"]["postal_code"] == other_fake_address.postal_code
    assert response_data["address"]["state"] == other_fake_address.state
