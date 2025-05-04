from httpx import AsyncClient
from tests.common.check_error_response import (
    check_unauthorized_response,
    check_not_found_response,
)


async def test_get_product_success(auth_client: AsyncClient, product_id: str):
    # Retrieve the product
    get_resp = await auth_client.get(f"/products/{product_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == product_id


async def test_get_product_not_found(auth_client: AsyncClient, fake_id: str):
    response = await auth_client.get(f"/products/{fake_id}")
    check_not_found_response(response, "Product", "product_id", fake_id)


async def test_get_product_unauthorized(client: AsyncClient, fake_id: str):
    response = await client.get(f"/products/{fake_id}")
    check_unauthorized_response(response)
