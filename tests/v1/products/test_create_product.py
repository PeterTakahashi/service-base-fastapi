import pytest
from httpx import AsyncClient
from faker import Faker
from tests.v1.modules.get_access_token import get_access_token
from tests.v1.modules.create_product import create_product

pytestmark = pytest.mark.asyncio
fake = Faker()

async def test_create_product_success(client: AsyncClient):
    access_token, _ = await get_access_token(client)
    product = await create_product(client, access_token, title="Test Product")
    assert product["title"] == "Test Product"
    assert "id" in product
    assert "created_at" in product
    assert "updated_at" in product
    assert product["episodes_count"] == 0


async def test_create_product_unauthorized(client: AsyncClient):
    resp = await client.post("/products/", json={"title": "Unauthorized Product"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Unauthorized"


async def test_create_product_duplicate_title(client: AsyncClient):
    access_token, _ = await get_access_token(client)

    title = "Duplicate Product"
    # 1st creation
    product = await create_product(client, access_token, title=title)

    # 2nd creation with the same title
    resp2 = await client.post(
        "/products/",
        json={"title": title},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp2.status_code == 409
    data = resp2.json()
    assert data == {
        'detail': {
            'errors':
                [
                    {
                        'status': '409',
                        'code': 'product_already_exists',
                        'title': 'Conflict',
                        'detail': "Product with title 'Duplicate Product' already exists.",
                        'source': {'pointer': '/title'}
                    }
                ]
        }
    }
