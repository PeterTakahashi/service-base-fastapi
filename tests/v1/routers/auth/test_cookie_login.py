from httpx import AsyncClient
from app.core.config import settings
from datetime import timedelta
from freezegun import freeze_time


async def test_cookie_login_success(client: AsyncClient, faker):
    """
    Test that a newly registered user can successfully log in via cookie authentication.
    """
    # 1. Create a user
    email = faker.unique.email()
    password = faker.password(length=12)
    await client.post(
        "/auth/register/register", json={"email": email, "password": password}
    )

    # 2. Log in with the user
    resp = await client.post(
        "/auth/cookie/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    # 3. Check the response
    assert resp.status_code == 204

    me = await client.get("/users/me")
    assert me.status_code == 200
    assert me.json()["email"] == email


async def test_cookie_login_bad_credentials(client: AsyncClient, faker):
    """
    Test that the login fails with status code 400 and 'LOGIN_BAD_CREDENTIALS'
    when the password is incorrect.
    """
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


async def test_cookie_login_lockout_reached(client: AsyncClient, faker):
    """
    Test that when the number of failed login attempts reaches the threshold,
    the account is locked. While locked, even a correct password will fail (HTTP 423).
    """
    # 1. Create a user
    email = faker.unique.email()
    password = faker.password(length=12)
    await client.post(
        "/auth/register/register",
        json={"email": email, "password": password},
    )

    # 2. Fail (max_attempts - 1) times
    max_attempts = settings.AUTHENTICATE_MAX_FAILED_ATTEMPTS
    for _ in range(max_attempts - 1):
        resp = await client.post(
            "/auth/cookie/login",
            data={"username": email, "password": "wrong-password"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == 400
        assert resp.json()["detail"] == "LOGIN_BAD_CREDENTIALS"

    # 3. Verify that we can still log in successfully before hitting the threshold
    resp = await client.post(
        "/auth/cookie/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 204

    me_resp = await client.get("/users/me")
    assert me_resp.status_code == 200

    # Log out
    await client.post("/auth/cookie/logout")

    # 4. Fail again up to the threshold
    for _ in range(max_attempts):
        resp = await client.post(
            "/auth/cookie/login",
            data={"username": email, "password": "wrong-password"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == 400
        assert resp.json()["detail"] == "LOGIN_BAD_CREDENTIALS"

    # 5. At this point, the account should be locked
    #    Even the correct password should fail
    resp = await client.post(
        "/auth/cookie/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 423
    assert resp.json()["detail"] == "LOGIN_ACCOUNT_LOCKED"

    # Accessing /users/me should return 401
    me_resp = await client.get("/users/me")
    assert me_resp.status_code == 401


async def test_cookie_login_failed_attempts_reset_after_time(
    client: AsyncClient, faker
):
    """
    Test that failed_attempts are reset after more than 30 minutes have passed since the last failed login.
    """
    email = faker.unique.email()
    password = faker.password(length=12)

    # 1. Register a new user
    create_resp = await client.post(
        "/auth/register/register",
        json={"email": email, "password": password},
    )
    assert create_resp.status_code == 201

    # 2. Fail login once
    resp = await client.post(
        "/auth/cookie/login",
        data={"username": email, "password": "wrong-pass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    # Should fail => 400 / "LOGIN_BAD_CREDENTIALS"
    assert resp.status_code == 400
    assert resp.json()["detail"] == "LOGIN_BAD_CREDENTIALS"

    # 3. Advance the current time by 31 minutes (30 + 1)
    with freeze_time() as frozen_time:
        frozen_time.tick(timedelta(minutes=31))

        # 4. Attempt another failed login
        #    If the counter was reset, this would count as the "first" failed attempt again
        resp = await client.post(
            "/auth/cookie/login",
            data={"username": email, "password": "wrong-pass-again"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == 400

        # 5. A correct password should now succeed
        resp = await client.post(
            "/auth/cookie/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        # Login success => 200 or 204
        assert resp.status_code == 204

        me_resp = await client.get("/users/me")
        assert me_resp.status_code == 200
        assert me_resp.json()["email"] == email


async def test_cookie_login_unlock_after_time(client: AsyncClient, faker):
    """
    Test that once the account is locked due to too many failures, waiting more than 30 minutes
    allows the user to log in successfully with the correct password (lock is lifted).
    """
    email = faker.unique.email()
    password = faker.password(length=12)

    # 1. Register a new user
    await client.post(
        "/auth/register/register",
        json={"email": email, "password": password},
    )

    # 2. Fail enough times to reach the lock threshold
    max_attempts = settings.AUTHENTICATE_MAX_FAILED_ATTEMPTS
    for _ in range(max_attempts):
        resp = await client.post(
            "/auth/cookie/login",
            data={"username": email, "password": "wrong-pass"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == 400
        assert resp.json()["detail"] == "LOGIN_BAD_CREDENTIALS"

    # 3. Confirm the account is locked - correct password => 423
    resp = await client.post(
        "/auth/cookie/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 423
    assert resp.json()["detail"] == "LOGIN_ACCOUNT_LOCKED"

    # 4. Advance the current time by 31 minutes to pass lock expiration
    with freeze_time() as frozen_time:
        frozen_time.tick(timedelta(minutes=31))

        # 5. Correct password => login success
        resp = await client.post(
            "/auth/cookie/login",
            data={"username": email, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert resp.status_code == 204

        me_resp = await client.get("/users/me")
        assert me_resp.status_code == 200
        assert me_resp.json()["email"] == email
