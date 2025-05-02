import pytest_asyncio
from tests.v1.fixtures.auth_fixture import access_token
from tests.v1.fixtures.client_fixture import client, auth_client
from tests.v1.fixtures.product_fixture import product, product_id
from uuid import uuid4

@pytest_asyncio.fixture
async def fake_id() -> str:
    return str(uuid4())
