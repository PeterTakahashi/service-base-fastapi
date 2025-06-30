from httpx import AsyncClient


async def test_get_me_authenticated(auth_client: AsyncClient):
    response = await auth_client.get("/users/me")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["email"] != ""
    assert response_data["id"] != ""
    assert "user_wallet" in response_data
    assert response_data["user_wallet"]["balance"] == "0.000000000"
    assert response_data["address"] is None
