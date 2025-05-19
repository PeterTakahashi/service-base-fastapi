from httpx import AsyncClient


async def test_cookie_login_success(client: AsyncClient, faker):
    # 1. create a user
    email = faker.unique.email()
    password = faker.password(length=12)
    await client.post(
        "/auth/register/register", json={"email": email, "password": password}
    )

    # 2. login with the user
    resp = await client.post(
        "/auth/cookie/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    # 3. check the response
    assert resp.status_code == 204

    me = await client.get("/users/me")
    assert me.status_code == 200
    assert me.json()["email"] == email


async def test_cookie_login_bad_credentials(client: AsyncClient, faker):
    email = faker.unique.email()
    password = faker.password(length=12)
    await client.post(
        "/auth/register/register", json={"email": email, "password": password}
    )

    resp = await client.post(
        "/auth/cookie/login",
        data={"username": email, "password": "wrong-password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert resp.status_code == 400
    assert resp.json()["detail"] == "LOGIN_BAD_CREDENTIALS"
