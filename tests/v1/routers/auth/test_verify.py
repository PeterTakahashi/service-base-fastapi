from httpx import AsyncClient
from tests.common.mailer import (
    get_latest_mail_source_by_recipient,
    get_password_reset_token_from_email_source,
)


async def test_verify_token_success(
    auth_client: AsyncClient, access_token: str, fake_email: str
):
    # 1. Request Verify the token
    await auth_client.post(
        "/auth/request-verify-token",
        json={"email": fake_email},
    )

    email_source = get_latest_mail_source_by_recipient(fake_email)
    token = get_password_reset_token_from_email_source(
        prefix="/verify-token/", source=email_source
    )

    # 2. Verify the token
    response = await auth_client.post(
        "/auth/verify",
        json={"token": token},
    )

    # 3. Check the response
    assert response.status_code == 200

    response = await auth_client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["email"] == fake_email
    assert response.json()["is_verified"] is True


async def test_verify_token_no_token(auth_client: AsyncClient):
    # 1. Verify the token without token
    response = await auth_client.post(
        "/auth/verify",
        json={},
    )

    # 2. Check the response
    assert response.status_code == 422


async def test_verify_token_no_header(client: AsyncClient):
    # 1. Verify the token without token
    response = await client.post(
        "/auth/verify",
        headers={},
        json={"token": "123456"},
    )

    # 2. Check the response
    assert response.status_code == 400
