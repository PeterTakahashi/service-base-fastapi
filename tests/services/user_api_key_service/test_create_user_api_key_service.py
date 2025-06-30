import pytest
from app.v1.schemas.user_api_key import UserApiKeyCreate, UserApiKeyRead
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_create_user_api_key_service(user_api_key_service, user):
    user_api_key_create = UserApiKeyCreate(
        name="Test API Key",
        expires_at=datetime.utcnow() + timedelta(days=30),
    )
    user_api_key = await user_api_key_service.create(
        user_id=user.id, user_api_key_create=user_api_key_create
    )
    assert user_api_key
    assert isinstance(user_api_key, UserApiKeyRead)
    assert user_api_key.name == user_api_key_create.name
    assert user_api_key.expires_at == user_api_key_create.expires_at
    assert user_api_key.api_key is not None
