import pytest
from app.v1.schemas.user_api_key import (
    UserApiKeyUpdate,
    UserApiKeyRead,
)
from sqlalchemy.exc import NoResultFound

user_api_key_update = UserApiKeyUpdate(
    name="Updated API Key Name",
    expires_at=None,
    allowed_origin=None,
    allowed_ip=None,
)


@pytest.mark.asyncio
async def test_update_user_api_key_service(user_api_key_service, user_api_key):
    user_api_key_updated = await user_api_key_service.update(
        user_api_key_id=user_api_key.id, user_api_key_update=user_api_key_update
    )
    assert user_api_key_updated
    assert isinstance(user_api_key_updated, UserApiKeyRead)
    assert user_api_key_updated.name == user_api_key_update.name


@pytest.mark.asyncio
async def test_not_found_update_user_api_key_service(user_api_key_service):
    with pytest.raises(NoResultFound):
        await user_api_key_service.update(
            user_api_key_id=0,  # Assuming this ID does not exist
            user_api_key_update=user_api_key_update,
        )


@pytest.mark.asyncio
async def test_soft_deleted_update_user_api_key_service(
    user_api_key_service, soft_deleted_user_api_key
):
    with pytest.raises(NoResultFound):
        await user_api_key_service.update(
            user_api_key_id=soft_deleted_user_api_key.id,
            user_api_key_update=user_api_key_update,
        )
