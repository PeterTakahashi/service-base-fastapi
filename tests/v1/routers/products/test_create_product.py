from httpx import AsyncClient
from tests.v1.common.unauthorized_response import check_unauthorized_response

async def test_create_product_success(auth_client: AsyncClient, product: dict):
    assert "title" in product
    assert "id" in product
    assert "created_at" in product
    assert "updated_at" in product

async def test_create_product_unauthorized(client: AsyncClient):
    response = await client.post("/products/", json={"title": "Unauthorized Product"})
    check_unauthorized_response(response)

async def test_create_product_duplicate_title(auth_client: AsyncClient, product: dict, product_id: str):
    title = product["title"]

    resp2 = await auth_client.post(
        "/products/",
        json={"title": title}
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
                    "detail": f"Product with title '{title}' already exists.",
                    "source": {"pointer": "/title"},
                }
            ]
        }
    }


async def test_create_product_empty_title(auth_client: AsyncClient):
    response = await auth_client.post(
        "/products/",
        json={"title": ""},
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


async def test_create_product_title_too_long(auth_client: AsyncClient):
    long_title = "A" * 256
    resp = await auth_client.post(
        "/products/",
        json={"title": long_title},
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


async def test_create_product_missing_title(auth_client: AsyncClient):
    resp = await auth_client.post(
        "/products/",
        json={},  # no title provided
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
