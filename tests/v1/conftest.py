import pytest_asyncio
from app.main import app
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

BASE_URL = "/app/v1"
@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=f"http://test{BASE_URL}") as async_client:
        yield async_client
