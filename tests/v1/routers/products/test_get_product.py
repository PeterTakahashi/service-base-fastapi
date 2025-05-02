from httpx import AsyncClient
from tests.v1.common.unauthorized_response import check_unauthorized_response

async def test_get_product_success(auth_client: AsyncClient, product_id: str):
    # Retrieve the product
    get_resp = await auth_client.get(f"/products/{product_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == product_id

async def test_get_product_not_found(auth_client: AsyncClient, fake_id: str):
    resp = await auth_client.get(
        f"/products/{fake_id}"
    )
    assert resp.status_code == 404
    body = resp.json()
    assert body["detail"] == {
        "errors": [
            {
                "status": "404",
                "code": "product_not_found",
                "title": "Not Found",
                "detail": f"Product with id '{fake_id}' not found.",
                "source": {"pointer": "/product_id"},
            }
        ]
    }


async def test_get_product_unauthorized(client: AsyncClient, fake_id: str):
    response = await client.get(f"/products/{fake_id}")
    check_unauthorized_response(response)
