from httpx import AsyncClient
from tests.v1.modules.create_product import create_product
from tests.v1.common.unauthorized_response import check_unauthorized_response

async def test_create_product_success(client: AsyncClient, access_token):
    product = await create_product(client, access_token, title="Test Product")
    assert product["title"] == "Test Product"
    assert "id" in product
    assert "created_at" in product
    assert "updated_at" in product
    assert product["episodes_count"] == 0


async def test_create_product_unauthorized(client: AsyncClient):
    response = await client.post("/products/", json={"title": "Unauthorized Product"})
    check_unauthorized_response(response)

async def test_create_product_duplicate_title(client: AsyncClient, access_token):
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


async def test_create_product_empty_title(client: AsyncClient, access_token):
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


async def test_create_product_title_too_long(client: AsyncClient, access_token):
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


async def test_create_product_missing_title(client: AsyncClient, access_token):
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
