import pytest

from sqlalchemy.exc import NoResultFound


@pytest.mark.asyncio
async def test_delete_user_api_key_service(
    user_api_key_service, user_api_key, user_api_key_repository
):
    result = await user_api_key_service.delete(user_api_key.id)
    assert result is None
    with pytest.raises(NoResultFound):
        await user_api_key_repository.find(id=user_api_key.id)


@pytest.mark.asyncio
async def test_delete_user_api_key_service_not_found(user_api_key_service):
    with pytest.raises(NoResultFound):
        await user_api_key_service.delete(0)


@pytest.mark.asyncio
async def test_already_deleted_user_api_key_service(
    user_api_key_service, soft_deleted_user_api_key, user_api_key_repository
):
    with pytest.raises(NoResultFound):
        await user_api_key_service.delete(soft_deleted_user_api_key.id)
    # Ensure the soft-deleted key still cannot be found
    with pytest.raises(NoResultFound):
        await user_api_key_repository.find(id=soft_deleted_user_api_key.id)
