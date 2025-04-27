import pytest
from httpx import AsyncClient
from tests.v1.modules.get_access_token import get_access_token
from tests.v1.modules.create_product import create_product

pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_index_products_authenticated(client: AsyncClient):
    access_token, _ = await get_access_token(client)
    await create_product(client, access_token, title="Test Product")

    # Get product list
    resp = await client.get(
        "/products/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, list)
    assert any(p["title"] == "Test Product" for p in data)


@pytest.mark.asyncio
async def test_index_products_with_title_filter(client: AsyncClient):
    access_token, _ = await get_access_token(client)

    # Create multiple products
    await create_product(client, access_token, title="1st Test Product Filter")
    await create_product(client, access_token, title="2nd Test Product")

    # Filter by title
    resp = await client.get(
        "/products/?title=Filter", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    results = resp.json()
    assert all("Filter" in p["title"] for p in results)


@pytest.mark.asyncio
async def test_index_products_pagination(client: AsyncClient):
    access_token, _ = await get_access_token(client)

    # Create 5 products
    for i in range(5):
        await create_product(client, access_token, title=f"Paginated Product {i}")

    # Get first 2
    resp1 = await client.get(
        "/products/?limit=2&offset=0",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert resp1.status_code == 200
    results1 = resp1.json()
    assert len(results1) == 2

    # Get next 2
    resp2 = await client.get(
        "/products/?limit=2&offset=2",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert resp2.status_code == 200
    results2 = resp2.json()
    assert len(results2) == 2

    # Ensure no overlap between page 1 and 2
    ids_page1 = {item["id"] for item in results1}
    ids_page2 = {item["id"] for item in results2}
    assert ids_page1.isdisjoint(ids_page2)


@pytest.mark.asyncio
async def test_index_products_unauthenticated(client: AsyncClient):
    resp = await client.get("/products/")
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Unauthorized"}
