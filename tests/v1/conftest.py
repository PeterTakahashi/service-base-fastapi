# pylint: disable=unused-import

import pytest_asyncio
from tests.v1.fixtures.auth_fixture import (
    access_token,
    fake_email,
    not_verified_access_token,
)
from tests.v1.fixtures.client_fixture import (
    client,
    auth_client,
    not_verified_auth_client,
)
from app.lib.utils.convert_id import encode_id


@pytest_asyncio.fixture
async def fake_id() -> str:
    return encode_id(0)
