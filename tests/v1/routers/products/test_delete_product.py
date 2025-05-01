import pytest
from httpx import AsyncClient
from uuid import uuid4
from tests.v1.modules.create_product import create_product
from tests.v1.common.unauthorized_response import check_unauthorized_response

async def test_delete_product_success(client: AsyncClient, access_token):
    product = await create_product(client, access_token)

    # Delete the product
    delete_resp = await client.delete(
        f"/products/{product['id']}", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert delete_resp.status_code == 204
    assert delete_resp.text == ""

    # Try to get the deleted product
    get_resp = await client.get(
        f"/products/{product['id']}", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert get_resp.status_code == 404
    assert get_resp.json()["detail"]["errors"][0]["code"] == "product_not_found"


async def test_delete_product_not_found(client: AsyncClient, access_token):
    invalid_id = str(uuid4())

    delete_resp = await client.delete(
        f"/products/{invalid_id}", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert delete_resp.status_code == 404
    assert delete_resp.json()["detail"]["errors"][0]["code"] == "product_not_found"


async def test_delete_product_unauthorized(client: AsyncClient):
    product_id = str(uuid4())
    response = await client.delete(f"/products/{product_id}")
    check_unauthorized_response(response)

