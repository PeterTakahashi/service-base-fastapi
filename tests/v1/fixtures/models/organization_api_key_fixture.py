import pytest_asyncio

from httpx import AsyncClient
from app.v1.schemas.organization_api_key.write import OrganizationApiKeyCreate
from app.lib.utils.convert_id import encode_id, decode_id


@pytest_asyncio.fixture
async def organization_api_key(
    auth_client: AsyncClient,
    organization,
    organization_api_key_repository,
    faker,
):
    organization_api_key_create = OrganizationApiKeyCreate(
        name=faker.word(),
        expires_at=None,
        allowed_origin=None,
        allowed_ip=None,
    )
    create_response = await auth_client.post(
        f"/organizations/{encode_id(organization.id)}/api-keys",
        json=organization_api_key_create.model_dump(),
    )
    organization_api_key_json = create_response.json()
    organization_api_key = await organization_api_key_repository.find(
        id=decode_id(organization_api_key_json["id"])
    )
    return organization_api_key
