from httpx import AsyncClient
from fastapi import status
from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode


async def test_cookie_logout_success(client: AsyncClient, faker):
    email = faker.unique.email()
    password = faker.password(length=12)
    await client.post(
        "/auth/register/register", json={"email": email, "password": password}
    )

    # 2. login with the user
    await client.post(
        "/auth/cookie/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    # 3. logout
    logout_resp = await client.post("/auth/cookie/logout")
    assert logout_resp.status_code == 204
    me = await client.get("/users/me")
    assert me.status_code == 401


async def test_cookie_logout_unauthorized(client: AsyncClient):
    resp = await client.post("/auth/cookie/logout")
    check_api_exception_response(
        resp,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail_code=ErrorCode.UNAUTHORIZED,
    )
