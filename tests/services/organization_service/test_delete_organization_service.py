import pytest
from sqlalchemy.exc import NoResultFound


@pytest.mark.asyncio
async def test_delete_organization_service(
    organization_service, organization, organization_repository
):
    result = await organization_service.delete(organization.id)
    assert result is None
    with pytest.raises(NoResultFound):
        await organization_repository.find(id=organization.id)


@pytest.mark.asyncio
async def test_delete_organization_service_not_found(organization_service):
    with pytest.raises(NoResultFound):
        await organization_service.delete(0)


@pytest.mark.asyncio
async def test_already_deleted_organization_service(
    organization_service, soft_deleted_organization, organization_repository
):
    with pytest.raises(NoResultFound):
        await organization_service.delete(soft_deleted_organization.id)
    # Ensure the soft-deleted organization still cannot be found
    with pytest.raises(NoResultFound):
        await organization_repository.find(id=soft_deleted_organization.id)
