import pytest
from app.v1.schemas.organization_api_key import (
    OrganizationApiKeyUpdate,
    OrganizationApiKeyRead,
)
from sqlalchemy.exc import NoResultFound

organization_api_key_update = OrganizationApiKeyUpdate(
    name="Updated API Key Name",
    expires_at=None,
    allowed_origin=None,
    allowed_ip=None,
)


@pytest.mark.asyncio
async def test_update_organization_api_key_service(
    organization_api_key_service, organization_api_key
):
    organization_api_key_updated = await organization_api_key_service.update(
        organization_api_key_id=organization_api_key.id,
        organization_api_key_update=organization_api_key_update,
    )
    assert organization_api_key_updated
    assert isinstance(organization_api_key_updated, OrganizationApiKeyRead)
    assert organization_api_key_updated.name == organization_api_key_update.name


@pytest.mark.asyncio
async def test_not_found_update_organization_api_key_service(
    organization_api_key_service,
):
    with pytest.raises(NoResultFound):
        await organization_api_key_service.update(
            organization_api_key_id=0,  # Assuming this ID does not exist
            organization_api_key_update=organization_api_key_update,
        )


@pytest.mark.asyncio
async def test_soft_deleted_update_organization_api_key_service(
    organization_api_key_service, soft_deleted_organization_api_key
):
    with pytest.raises(NoResultFound):
        await organization_api_key_service.update(
            organization_api_key_id=soft_deleted_organization_api_key.id,
            organization_api_key_update=organization_api_key_update,
        )
