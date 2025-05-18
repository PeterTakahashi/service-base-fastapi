from httpx import AsyncClient
from tests.common.mailer import (
    get_latest_mail_source_by_recipient,
    get_password_reset_token_from_email_source,
)


async def test_reset_password_success(client: AsyncClient, faker):
    # 1. create a user
    email = faker.unique.email()
    password = faker.password(length=12)
    await client.post(
        "/auth/register/register", json={"email": email, "password": password}
    )

    # 2. request a password reset
    await client.post(
        "/auth/forgot-password",
        json={"email": email},
    )
    # 3. get the latest email
    email_source = get_latest_mail_source_by_recipient(email)
    token = get_password_reset_token_from_email_source(
        prefix="/reset-password/", source=email_source
    )

    # 4. reset the password
    new_password = faker.password(length=12)
    response = await client.post(
        "/auth/reset-password",
        json={"token": token, "password": new_password},
    )

    # 5. check the response
    assert response.status_code == 200

    # 6. login with the new password
    response = await client.post(
        "/auth/jwt/login",
        data={"username": email, "password": new_password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert "access_token" in body and body["access_token"]


async def test_reset_password_invalid_token(client: AsyncClient, faker):
    new_password = faker.password(length=12)
    token = faker.uuid4()
    response = await client.post(
        "/auth/reset-password",
        json={"token": token, "password": new_password},
    )
    assert response.status_code == 400
