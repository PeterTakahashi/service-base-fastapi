import pytest
from httpx import AsyncClient
from uuid import uuid4
from tests.v1.modules.get_access_token import get_access_token
from tests.v1.modules.create_product import create_product

pytestmark = pytest.mark.asyncio

async def test_get_product_success(client: AsyncClient):
    token, _ = await get_access_token(client)
    product = await create_product(client, token, title="Test Product")

    # Retrieve the product
    get_resp = await client.get(
        f"/products/{product['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == product['id']
    assert data["title"] == "Test Product"

async def test_get_product_not_found(client: AsyncClient):
    token, _ = await get_access_token(client)
    invalid_id = str(uuid4())

    resp = await client.get(
        f"/products/{invalid_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 404
    body = resp.json()
    assert body["detail"] == {'errors': [{'status': '404', 'code': 'product_not_found', 'title': 'Not Found', 'detail': f"Product with id '{invalid_id}' not found.", 'source': {'pointer': '/product_id'}}]}

async def test_get_product_unauthorized(client: AsyncClient):
    resp = await client.get(f"/products/{str(uuid4())}")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Unauthorized"
