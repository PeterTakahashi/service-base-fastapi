import pytest
from sqlalchemy.exc import NoResultFound


@pytest.mark.asyncio
async def test_delete_organization_api_key_service(
    organization_api_key_service, organization_api_key, organization_api_key_repository
):
    result = await organization_api_key_service.delete(organization_api_key.id)
    assert result is None
    with pytest.raises(NoResultFound):
        await organization_api_key_repository.find(id=organization_api_key.id)


@pytest.mark.asyncio
async def test_delete_organization_api_key_service_not_found(
    organization_api_key_service,
):
    with pytest.raises(NoResultFound):
        await organization_api_key_service.delete(0)


@pytest.mark.asyncio
async def test_already_deleted_organization_api_key_service(
    organization_api_key_service,
    soft_deleted_organization_api_key,
    organization_api_key_repository,
):
    with pytest.raises(NoResultFound):
        await organization_api_key_service.delete(soft_deleted_organization_api_key.id)
    # Ensure the soft-deleted key still cannot be found
    with pytest.raises(NoResultFound):
        await organization_api_key_repository.find(
            id=soft_deleted_organization_api_key.id
        )
