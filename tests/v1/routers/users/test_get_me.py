from httpx import AsyncClient


async def test_get_me_authenticated(auth_client: AsyncClient):
    response = await auth_client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["email"] != ""
    assert response.json()["id"] != ""
    assert "user_wallet" in response.json()
    assert response.json()["user_wallet"]["balance"] == "0.000000000"
