import pytest_asyncio

from httpx import AsyncClient
from app.v1.schemas.organization import OrganizationCreate
from app.lib.utils.convert_id import decode_id


@pytest_asyncio.fixture
async def organization(auth_client: AsyncClient, faker, organization_repository):
    organization_data = OrganizationCreate(
        name=faker.company(),
        description=faker.sentence(),
        profile_image_key="test_profile_image_key",
        billing_email=faker.email(),
    )
    response = await auth_client.post(
        "/organizations", json=organization_data.model_dump()
    )
    # Assert
    assert response.status_code == 201
    response_data = response.json()
    organization = await organization_repository.find(id=decode_id(response_data["id"]))
    return organization
