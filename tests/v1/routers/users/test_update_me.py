from httpx import AsyncClient
from tests.common.check_error_response import (
    check_validation_error_response,
)
from fastapi import status
from tests.common.check_error_response import check_api_exception_response


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
    check_validation_error_response(
        response,
        path="/users/me",
        errors=[
            {
                "status": "422",
                "code": "update_user_email_already_exists",
                "title": "User Email Already Exists",
                "detail": "The email address you are trying to use is already associated with another account. Please use a different email address.",
                "source": {},
            }
        ],
    )


async def test_update_me_unauthenticated(client: AsyncClient):
    response = await client.patch("/users/me", json={"email": "test@test.com"})
    check_api_exception_response(
        response, status_code=status.HTTP_401_UNAUTHORIZED, detail_code="unauthorized"
    )
