from httpx import AsyncClient


async def test_request_verify_token_success(
    client: AsyncClient, access_token: str, fake_email: str
):
    # 1. Verify the token
    response = await client.post(
        "/auth/request-verify-token",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"email": fake_email},
    )

    # 2. Check the response
    assert response.status_code == 202


async def test_request_verify_token_no_header(client: AsyncClient, fake_email: str):
    # 1. Verify the token without authorization
    response = await client.post(
        "/auth/request-verify-token",
        headers={},
        json={"email": fake_email},
    )
    # 2. Check the response
    assert response.status_code == 202


async def test_request_verify_token_no_email(client: AsyncClient, access_token: str):
    # 1. Verify the token without email
    response = await client.post(
        "/auth/request-verify-token",
        headers={"Authorization": f"Bearer {access_token}"},
        json={},
    )
    # 2. Check the response
    assert response.status_code == 422
