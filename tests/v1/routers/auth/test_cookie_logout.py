from httpx import AsyncClient


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
    logout_resp = await client.post("/auth/cookie/logout")
    assert logout_resp.status_code == 401
    resp_json = logout_resp.json()
    assert resp_json == {
        "errors": [
            {
                "code": "unauthorized",
                "detail": "Authentication credentials were not provided or are invalid.",
                "status": "401",
                "title": "Unauthorized",
            }
        ]
    }
