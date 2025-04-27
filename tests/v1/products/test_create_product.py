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
    assert resp.json() == {
        'errors': [
            {
                'code': 'unauthorized',
                'detail': 'Authentication credentials were not provided or are invalid.',
                'status': '401',
                'title': 'Unauthorized'
            }
        ]
    }


async def test_create_product_duplicate_title(client: AsyncClient):
    access_token, _ = await get_access_token(client)

    title = "Duplicate Product"
    # 1st creation
    await create_product(client, access_token, title=title)

    # 2nd creation with the same title
    resp2 = await client.post(
        "/products/",
        json={"title": title},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert resp2.status_code == 409
    data = resp2.json()
    assert data == {
        "detail": {
            "errors": [
                {
                    "status": "409",
                    "code": "product_already_exists",
                    "title": "Conflict",
                    "detail": "Product with title 'Duplicate Product' already exists.",
                    "source": {"pointer": "/title"},
                }
            ]
        }
    }


async def test_create_product_empty_title(client: AsyncClient):
    access_token, _ = await get_access_token(client)
    response = await client.post(
        "/products/",
        json={"title": ""},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    data = response.json()
    assert response.status_code == 422
    assert data == {
        'errors': [
            {
                'status': '422',
                'code': 'validation_error',
                'title': 'Validation Error',
                'detail': 'String should have at least 1 character',
                'source': {'pointer': '/title'}
            }
        ]
    }


async def test_create_product_title_too_long(client: AsyncClient):
    access_token, _ = await get_access_token(client)
    long_title = "A" * 256
    resp = await client.post(
        "/products/",
        json={"title": long_title},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert resp.status_code == 422
    data = resp.json()
    assert data == {
        'errors': [
            {
                'status': '422',
                'code': 'validation_error',
                'title': 'Validation Error',
                'detail': 'String should have at most 100 characters',
                'source': {'pointer': '/title'}
            }
        ]
    }


async def test_create_product_missing_title(client: AsyncClient):
    access_token, _ = await get_access_token(client)
    resp = await client.post(
        "/products/",
        json={},  # no title provided
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert resp.status_code == 422
    data = resp.json()
    assert data == {
        'errors': [
            {
                'status': '422',
                'code': 'validation_error',
                'title': 'Validation Error',
                'detail': 'Field required',
                'source': {'pointer': '/title'}
            }
        ]
    }
