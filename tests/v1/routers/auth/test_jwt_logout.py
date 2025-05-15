from httpx import AsyncClient


async def test_logout_success(client: AsyncClient, access_token):
    logout_resp = await client.post(
        "/auth/jwt/logout", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert logout_resp.status_code == 204

    me = await client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert me.status_code == 200


async def test_logout_unauthorized(client: AsyncClient):
    # Authorization ヘッダーなしでログアウトを試みる
    logout_resp = await client.post("/auth/jwt/logout")

    # 401 Unauthorized を期待
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
