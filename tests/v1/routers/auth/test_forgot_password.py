from httpx import AsyncClient


async def test_forgot_password_success(client: AsyncClient, faker):
    # 1. create a user
    email = faker.unique.email()
    password = faker.password(length=12)
    await client.post(
        "/auth/register/register", json={"email": email, "password": password}
    )

    # 2. request a password reset
    response = await client.post(
        "/auth/forgot-password",
        json={"email": email},
    )

    # 3. check the response
    assert response.status_code == 202


async def test_forgot_password_user_not_found(client: AsyncClient, faker):
    # 1. request a password reset for a non-existent user
    response = await client.post(
        "/auth/forgot-password",
        json={"email": faker.unique.email()},
    )
    # 2. check the response
    assert response.status_code == 202
