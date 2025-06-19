from httpx import AsyncClient


async def test_get_me_authenticated(auth_client: AsyncClient):
    response = await auth_client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["email"] != ""
    assert response.json()["id"] != ""
    assert "wallet" in response.json()
    assert response.json()["wallet"]["balance"] == 0
