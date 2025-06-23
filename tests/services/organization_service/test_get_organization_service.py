import pytest
from sqlalchemy.exc import NoResultFound


@pytest.mark.asyncio
async def test_get_organization_service(
    organization_service, organization, organization_repository
):
    organization_read = await organization_service.get(organization.id)

    assert organization_read.id == organization.id
    assert organization_read.name == organization.name


@pytest.mark.asyncio
async def test_get_organization_service_not_found(organization_service):
    with pytest.raises(NoResultFound):
        await organization_service.get(0)
