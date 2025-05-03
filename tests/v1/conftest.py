import pytest_asyncio
from tests.v1.fixtures.auth_fixture import access_token
from tests.v1.fixtures.client_fixture import client, auth_client
from tests.v1.fixtures.product_fixture import product, product_id
from tests.v1.fixtures.character_fixture import character
from app.lib.convert_id import encode_id

@pytest_asyncio.fixture
async def fake_id() -> str:
    return encode_id(0)
