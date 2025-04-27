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
    resp = await client.post(
        "/products/",
        json={"title": ""},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert resp.status_code == 422
    data = resp.json()
    assert any(
        err["loc"] == ["body", "title"] and "at least 1 character" in err["msg"]
        for err in data["detail"]
    )


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
    assert any(
        err["loc"] == ["body", "title"] and "at most 100 characters" in err["msg"]
        for err in data["detail"]
    )


async def test_create_product_missing_title(client: AsyncClient):
    access_token, _ = await get_access_token(client)
    resp = await client.post(
        "/products/",
        json={},  # title キーがない
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert resp.status_code == 422
    data = resp.json()
    assert any(
        err["loc"] == ["body", "title"] and "field required" in err["msg"].lower()
        for err in data["detail"]
    )
