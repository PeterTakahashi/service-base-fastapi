from httpx import AsyncClient
from tests.common.check_error_response import (
    check_unauthorized_response,
    check_not_found_response,
)


async def test_update_product_success(auth_client: AsyncClient, product_id: str):
    update_resp = await auth_client.put(
        f"/products/{product_id}", json={"title": "Updated Title"}
    )
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["id"] == product_id
    assert data["title"] == "Updated Title"


async def test_update_product_not_found(auth_client: AsyncClient, fake_id: str):
    response = await auth_client.put(
        f"/products/{fake_id}",
        json={"title": "New Title"},
    )
    check_not_found_response(response, "Product", "/product_id", fake_id)


async def test_update_product_unauthorized(client: AsyncClient, fake_id: str):
    resp = await client.put(f"/products/{fake_id}", json={"title": "Unauthorized"})
    check_unauthorized_response(resp)


async def test_update_product_empty_title(auth_client: AsyncClient, product_id: str):
    resp = await auth_client.put(
        f"/products/{product_id}",
        json={"title": ""},
    )
    assert resp.status_code == 422
    data = resp.json()
    assert data == {
        "errors": [
            {
                "status": "422",
                "code": "validation_error",
                "title": "Validation Error",
                "detail": "String should have at least 1 character",
                "source": {"pointer": "/title"},
            }
        ]
    }


async def test_update_product_title_too_long(auth_client: AsyncClient, product_id: str):
    long_title = "A" * 256

    resp = await auth_client.put(
        f"/products/{product_id}",
        json={"title": long_title},
    )
    assert resp.status_code == 422
    data = resp.json()
    assert data == {
        "errors": [
            {
                "status": "422",
                "code": "validation_error",
                "title": "Validation Error",
                "detail": "String should have at most 100 characters",
                "source": {"pointer": "/title"},
            }
        ]
    }


async def test_update_product_missing_title(auth_client: AsyncClient, product_id: str):
    resp = await auth_client.put(
        f"/products/{product_id}",
        json={},  # no title provided
    )
    assert resp.status_code == 422
    data = resp.json()
    assert data == {
        "errors": [
            {
                "status": "422",
                "code": "validation_error",
                "title": "Validation Error",
                "detail": "Field required",
                "source": {"pointer": "/title"},
            }
        ]
    }
