from httpx import AsyncClient
from uuid import uuid4
from tests.v1.modules.create_product import create_product
from tests.v1.common.unauthorized_response import check_unauthorized_response

async def test_get_product_success(client: AsyncClient, access_token):
    product = await create_product(client, access_token, title="Test Product")

    # Retrieve the product
    get_resp = await client.get(
        f"/products/{product['id']}", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == product["id"]
    assert data["title"] == "Test Product"


async def test_get_product_not_found(client: AsyncClient, access_token):
    invalid_id = str(uuid4())

    resp = await client.get(
        f"/products/{invalid_id}", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 404
    body = resp.json()
    assert body["detail"] == {
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


async def test_get_product_unauthorized(client: AsyncClient):
    response = await client.get(f"/products/{str(uuid4())}")
    check_unauthorized_response(response)