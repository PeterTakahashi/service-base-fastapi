from httpx import AsyncClient
from tests.v1.modules.create_product import create_product
from uuid import uuid4
from tests.v1.common.unauthorized_response import check_unauthorized_response

async def test_update_product_success(client: AsyncClient, access_token):
    product = await create_product(client, access_token, title="Original Title")
    product_id = product["id"]

    # Update product
    update_resp = await client.put(
        f"/products/{product_id}",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["id"] == product_id
    assert data["title"] == "Updated Title"

async def test_update_product_not_found(client: AsyncClient, access_token):
    invalid_id = str(uuid4())

    update_resp = await client.put(
        f"/products/{invalid_id}",
        json={"title": "New Title"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert update_resp.status_code == 404
    assert update_resp.json()["detail"] == {
        "errors": [
            {
                "status": "404",
                "code": "product_not_found",
                "title": "Not Found",
                "detail": f"Product with id '{invalid_id}' not found.",
                "source": {"pointer": "/product_id"},
            }
        ]
    }


async def test_update_product_unauthorized(client: AsyncClient):
    product_id = str(uuid4())
    resp = await client.put(f"/products/{product_id}", json={"title": "Unauthorized"})
    check_unauthorized_response(resp)

async def test_update_product_empty_title(client: AsyncClient, access_token):
    product = await create_product(client, access_token, title="Before")
    product_id = product["id"]

    resp = await client.put(
        f"/products/{product_id}",
        json={"title": ""},
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
                'detail': 'String should have at least 1 character',
                'source': {'pointer': '/title'},
            }
        ]
    }


async def test_update_product_title_too_long(client: AsyncClient, access_token):
    product = await create_product(client, access_token, title="Before")
    product_id = product["id"]
    long_title = "A" * 256

    resp = await client.put(
        f"/products/{product_id}",
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
                'source': {'pointer': '/title'},
            }
        ]
    }


async def test_update_product_missing_title(client: AsyncClient, access_token):
    product = await create_product(client, access_token, title="Before")
    product_id = product["id"]

    resp = await client.put(
        f"/products/{product_id}",
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
                'source': {'pointer': '/title'},
            }
        ]
    }
