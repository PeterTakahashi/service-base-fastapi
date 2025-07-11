"""
Fixtures for testing FastAPI application.
"""

from typing import AsyncGenerator  # Standard library import
import pytest_asyncio  # Third-party imports
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from main import app  # Local application import
from copy import copy

BASE_URL = "/app/v1"


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture to provide an HTTP client for testing.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url=f"http://test{BASE_URL}"
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient, access_token: str) -> AsyncClient:
    """
    Fixture to provide an authenticated HTTP client for testing.
    """
    authenticated_client = client  # Avoid name collision
    authenticated_client.headers.update({"Authorization": f"Bearer {access_token}"})
    return authenticated_client


@pytest_asyncio.fixture
async def not_verified_auth_client(
    client: AsyncClient, not_verified_access_token: str
) -> AsyncClient:
    """
    Fixture to provide an authenticated HTTP client for testing.
    """
    authenticated_client = client
    authenticated_client.headers.update(
        {"Authorization": f"Bearer {not_verified_access_token}"}
    )
    return authenticated_client


@pytest_asyncio.fixture
async def other_auth_client(
    client: AsyncClient, other_access_token: str
) -> AsyncClient:
    copied_client = copy(client)
    copied_client.headers = client.headers.copy()
    copied_client.headers.update({"Authorization": f"Bearer {other_access_token}"})
    return copied_client
