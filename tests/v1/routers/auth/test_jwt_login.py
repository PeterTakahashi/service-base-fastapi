from httpx import AsyncClient
from fastapi_users.router.common import ErrorCode
from tests.common.check_error_response import check_unauthorized_response


async def test_jwt_login_success(client: AsyncClient, faker):
    # 1. create a user
    email = faker.unique.email()
    password = faker.password(length=12)
    await client.post(
        "/auth/register/register", json={"email": email, "password": password}
    )

    # 2. login with the user
    resp = await client.post(
        "/auth/jwt/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    # 3. check the response
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert "access_token" in body and body["access_token"]

    me = await client.get(
        "/users/me", headers={"Authorization": f"Bearer {body['access_token']}"}
    )
    assert me.status_code == 200
    assert me.json()["email"] == email


async def test_jwt_login_bad_credentials(client: AsyncClient, faker):
    email = faker.unique.email()
    password = faker.password(length=12)
    await client.post(
        "/auth/register/register", json={"email": email, "password": password}
    )

    resp = await client.post(
        "/auth/jwt/login",
        data={"username": email, "password": "wrong-password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    check_unauthorized_response(
        resp, code=ErrorCode.LOGIN_BAD_CREDENTIALS.lower(), path="/auth/jwt/login"
    )
