import pytest
from httpx import AsyncClient
from uuid import uuid4
from tests.v1.modules.get_access_token import get_access_token
from tests.v1.modules.create_product import create_product

pytestmark = pytest.mark.asyncio


async def test_delete_product_success(client: AsyncClient):
    token, _ = await get_access_token(client)
    product = await create_product(client, token)

    # Delete the product
    delete_resp = await client.delete(
        f"/products/{product['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_resp.status_code == 204

    # Try to get the deleted product
    get_resp = await client.get(
        f"/products/{product['id']}", headers={"Authorization": f"Bearer {token}"}
    )
    assert get_resp.status_code == 404
    assert get_resp.json()["detail"]["errors"][0]["code"] == "product_not_found"


async def test_delete_product_not_found(client: AsyncClient):
    token, _ = await get_access_token(client)
    invalid_id = str(uuid4())

    delete_resp = await client.delete(
        f"/products/{invalid_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_resp.status_code == 404
    assert delete_resp.json()["detail"]["errors"][0]["code"] == "product_not_found"


async def test_delete_product_unauthorized(client: AsyncClient):
    product_id = str(uuid4())
    resp = await client.delete(f"/products/{product_id}")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Unauthorized"
