import pytest
from app.v1.schemas.user_api_key import UserApiKeyListRead, UserApiKeySearchParams
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_get_list_user_api_key_service(
    user_api_key_service, user_api_key_repository, user_api_keys, user
):
    search_params = UserApiKeySearchParams(
        limit=10, offset=0, sorted_by="created_at", sorted_order="desc"
    )

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == len(user_api_keys)
    assert result.meta.total_count == len(user_api_keys)

    for api_key in result.data:
        assert api_key.id in [key.id for key in user_api_keys]


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_name__icontains(
    user_api_key_service, user_api_key_repository, user_api_keys, user
):
    search_params = UserApiKeySearchParams(
        limit=10,
        offset=0,
        sorted_by="created_at",
        sorted_order="desc",
        name__icontains=user_api_keys[0].name,
    )

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_api_key__icontains(
    user_api_key_service, user_api_key_repository, user_api_keys, user
):
    search_params = UserApiKeySearchParams(
        limit=10,
        offset=0,
        sorted_by="created_at",
        sorted_order="desc",
        api_key__icontains=user_api_keys[0].api_key,
    )

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_expires_at__gte_exists(
    user_api_key_service,
    user_api_key_repository,
    user_api_key,
    expired_user_api_key,
    user,
):
    search_params = UserApiKeySearchParams(expires_at__gte=datetime.utcnow())

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_expires_at__gte_not_exists(
    user_api_key_service, user_api_key_repository, expired_user_api_key, user
):
    search_params = UserApiKeySearchParams(expires_at__gte=datetime.utcnow())

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_expires_at__lte_exists(
    user_api_key_service, user_api_key_repository, expired_user_api_key, user
):
    search_params = UserApiKeySearchParams(expires_at__lte=datetime.utcnow())

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_expires_at__lte_not_exists(
    user_api_key_service, user_api_key_repository, user_api_key, user
):
    search_params = UserApiKeySearchParams(expires_at__lte=datetime.utcnow())

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_allowed_origin__icontains(
    user_api_key_service, user_api_key_repository, user_api_keys, user
):
    search_params = UserApiKeySearchParams(
        allowed_origin__icontains=user_api_keys[0].allowed_origin
    )

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_allowed_ip__icontains(
    user_api_key_service, user_api_key_repository, user_api_keys, user
):
    search_params = UserApiKeySearchParams(
        allowed_ip__icontains=user_api_keys[0].allowed_ip
    )

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_created_at__gte_exists(
    user_api_key_service, user_api_key_repository, user_api_key, user
):
    search_params = UserApiKeySearchParams(created_at__gte=user_api_key.created_at)

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_created_at__gte_not_exists(
    user_api_key_service, user_api_key_repository, expired_user_api_key, user
):
    search_params = UserApiKeySearchParams(created_at__gte=datetime.utcnow())

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_created_at__lte_exists(
    user_api_key_service, user_api_key_repository, expired_user_api_key, user
):
    search_params = UserApiKeySearchParams(
        created_at__lte=expired_user_api_key.created_at
    )

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_created_at__lte_not_exists(
    user_api_key_service, user_api_key_repository, user_api_key, user
):
    search_params = UserApiKeySearchParams(
        created_at__lte=datetime.utcnow() - timedelta(days=1)
    )

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_updated_at__gte_exists(
    user_api_key_service, user_api_key_repository, user_api_key, user
):
    search_params = UserApiKeySearchParams(updated_at__gte=user_api_key.updated_at)

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_updated_at__gte_not_exists(
    user_api_key_service, user_api_key_repository, expired_user_api_key, user
):
    search_params = UserApiKeySearchParams(updated_at__gte=datetime.utcnow())

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 0


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_updated_at__lte_exists(
    user_api_key_service, user_api_key_repository, expired_user_api_key, user
):
    search_params = UserApiKeySearchParams(
        updated_at__lte=expired_user_api_key.updated_at
    )

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 1


@pytest.mark.asyncio
async def test_get_list_user_api_key_service_filter_updated_at__lte_not_exists(
    user_api_key_service, user_api_key_repository, user_api_key, user
):
    search_params = UserApiKeySearchParams(
        updated_at__lte=datetime.utcnow() - timedelta(days=1)
    )

    result = await user_api_key_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(result, UserApiKeyListRead)
    assert len(result.data) == 0
