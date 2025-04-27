import pytest
from httpx import AsyncClient
from faker import Faker
from tests.v1.modules.get_access_token import get_access_token

pytestmark = pytest.mark.asyncio
fake = Faker()


@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient):
    access_token, email = await get_access_token(client)

    # 2. Logout with valid token
    logout_resp = await client.post(
        "/auth/jwt/logout", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert logout_resp.status_code == 204

    # 3. Access protected endpoint after logout (still works since FastAPIUsers doesn't invalidate token)
    me = await client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert (
        me.status_code == 200
    )  # token is stateless; still works unless you implement token revocation


async def test_logout_unauthorized(client: AsyncClient):
    # Authorization ヘッダーなしでログアウトを試みる
    logout_resp = await client.post("/auth/jwt/logout")

    # 401 Unauthorized を期待
    assert logout_resp.status_code == 401
    resp_json = logout_resp.json()
    assert "detail" in resp_json
