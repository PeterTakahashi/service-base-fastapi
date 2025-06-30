import pytest
from app.v1.schemas.organization_api_key import (
    OrganizationApiKeyListRead,
    OrganizationApiKeySearchParams,
)
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service(
    organization_api_key_service,
    organization_api_key_repository,
    organization_api_keys,
    organization,
):
    search_params = OrganizationApiKeySearchParams(
        limit=10, offset=0, sorted_by="created_at", sorted_order="desc"
    )

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == len(organization_api_keys)
    assert result.meta.total_count == len(organization_api_keys)

    for api_key in result.data:
        assert api_key.id in [key.id for key in organization_api_keys]


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_name__icontains(
    organization_api_key_service,
    organization_api_key_repository,
    organization_api_keys,
    organization,
):
    search_params = OrganizationApiKeySearchParams(
        limit=10,
        offset=0,
        sorted_by="created_at",
        sorted_order="desc",
        name__icontains=organization_api_keys[0].name,
    )

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_api_key__icontains(
    organization_api_key_service,
    organization_api_key_repository,
    organization_api_keys,
    organization,
):
    search_params = OrganizationApiKeySearchParams(
        limit=10,
        offset=0,
        sorted_by="created_at",
        sorted_order="desc",
        api_key__icontains=organization_api_keys[0].api_key,
    )

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_expires_at__gte_exists(
    organization_api_key_service,
    organization_api_key_repository,
    organization_api_key,
    expired_organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(expires_at__gte=datetime.utcnow())

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_expires_at__gte_not_exists(
    organization_api_key_service,
    organization_api_key_repository,
    expired_organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(expires_at__gte=datetime.utcnow())

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_expires_at__lte_exists(
    organization_api_key_service,
    organization_api_key_repository,
    expired_organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(expires_at__lte=datetime.utcnow())

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_expires_at__lte_not_exists(
    organization_api_key_service,
    organization_api_key_repository,
    organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(expires_at__lte=datetime.utcnow())

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_allowed_origin__icontains(
    organization_api_key_service,
    organization_api_key_repository,
    organization_api_keys,
    organization,
):
    search_params = OrganizationApiKeySearchParams(
        allowed_origin__icontains=organization_api_keys[0].allowed_origin
    )

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_allowed_ip__icontains(
    organization_api_key_service,
    organization_api_key_repository,
    organization_api_keys,
    organization,
):
    search_params = OrganizationApiKeySearchParams(
        allowed_ip__icontains=organization_api_keys[0].allowed_ip
    )

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_created_at__gte_exists(
    organization_api_key_service,
    organization_api_key_repository,
    organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(
        created_at__gte=organization_api_key.created_at
    )

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_created_at__gte_not_exists(
    organization_api_key_service,
    organization_api_key_repository,
    expired_organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(created_at__gte=datetime.utcnow())

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_created_at__lte_exists(
    organization_api_key_service,
    organization_api_key_repository,
    expired_organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(
        created_at__lte=expired_organization_api_key.created_at
    )

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_created_at__lte_not_exists(
    organization_api_key_service,
    organization_api_key_repository,
    organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(
        created_at__lte=datetime.utcnow() - timedelta(days=1)
    )

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_updated_at__gte_exists(
    organization_api_key_service,
    organization_api_key_repository,
    organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(
        updated_at__gte=organization_api_key.updated_at
    )

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_updated_at__gte_not_exists(
    organization_api_key_service,
    organization_api_key_repository,
    expired_organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(updated_at__gte=datetime.utcnow())

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_updated_at__lte_exists(
    organization_api_key_service,
    organization_api_key_repository,
    expired_organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(
        updated_at__lte=expired_organization_api_key.updated_at
    )

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_organization_api_key_service_filter_updated_at__lte_not_exists(
    organization_api_key_service,
    organization_api_key_repository,
    organization_api_key,
    organization,
):
    search_params = OrganizationApiKeySearchParams(
        updated_at__lte=datetime.utcnow() - timedelta(days=1)
    )

    result = await organization_api_key_service.get_list(
        organization_id=organization.id, search_params=search_params
    )

    assert isinstance(result, OrganizationApiKeyListRead)
    assert len(result.data) == 0
