from httpx import AsyncClient
from tests.v1.common.unauthorized_response import check_unauthorized_response

async def test_delete_product_success(auth_client: AsyncClient, product_id: str):
    # Delete the product
    response = await auth_client.delete(f"/products/{product_id}")
    assert response.status_code == 204
    assert response.text == ""

    # Try to get the deleted product
    get_resp = await auth_client.get(f"/products/{product_id}")
    assert get_resp.status_code == 404
    assert get_resp.json()["detail"]["errors"][0]["code"] == "product_not_found"

async def test_delete_product_not_found(auth_client: AsyncClient, fake_id: str):
    response = await auth_client.delete(f"/products/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"]["errors"][0]["code"] == "product_not_found"

async def test_delete_product_unauthorized(client: AsyncClient, fake_id: str):
    response = await client.delete(f"/products/{fake_id}")
    check_unauthorized_response(response)
