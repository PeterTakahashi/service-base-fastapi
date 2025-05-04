import pytest_asyncio
from main import app
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from typing import AsyncGenerator

BASE_URL = "/app/v1"


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url=f"http://test{BASE_URL}"
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient, access_token: str) -> AsyncClient:
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client
