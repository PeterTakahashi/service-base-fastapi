import pytest
from httpx import AsyncClient
from tests.v1.modules.create_product import create_product
from tests.v1.common.unauthorized_response import check_unauthorized_response


@pytest.mark.asyncio
async def test_index_products_authenticated(auth_client: AsyncClient, product: dict):
    resp = await auth_client.get("/products/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert any(p["title"] == product["title"] for p in data)


@pytest.mark.asyncio
async def test_index_products_with_title_filter(auth_client: AsyncClient):
    await create_product(auth_client, title="1st Test Product Filter")
    await create_product(auth_client, title="2nd Test Product")

    # Filter by title
    resp = await auth_client.get("/products/?title=Filter")
    assert resp.status_code == 200
    results = resp.json()
    assert all("Filter" in p["title"] for p in results)


@pytest.mark.asyncio
async def test_index_products_pagination(auth_client: AsyncClient):
    # Create 5 products
    for i in range(5):
        await create_product(auth_client, title=f"Paginated Product {i}")

    # Get first 2
    resp1 = await auth_client.get("/products/?limit=2&offset=0")
    assert resp1.status_code == 200
    results1 = resp1.json()
    assert len(results1) == 2

    # Get next 2
    resp2 = await auth_client.get("/products/?limit=2&offset=2")
    assert resp2.status_code == 200
    results2 = resp2.json()
    assert len(results2) == 2

    # Ensure no overlap between page 1 and 2
    ids_page1 = {item["id"] for item in results1}
    ids_page2 = {item["id"] for item in results2}
    assert ids_page1.isdisjoint(ids_page2)


@pytest.mark.asyncio
async def test_index_products_unauthenticated(client: AsyncClient):
    response = await client.get("/products/")
    check_unauthorized_response(response)
