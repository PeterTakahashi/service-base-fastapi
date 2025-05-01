import pytest_asyncio
from app.v1.services.user_service import UserService
from app.v1.schemas.user import UserUpdate, UserRead

@pytest_asyncio.fixture
async def user_service(user_repository):
    return UserService(user_repository)

async def test_get_me(user_service, user):
    result = await user_service.get_me(user)
    assert isinstance(result, UserRead)
    assert result.id == user.id
    assert result.email == user.email

async def test_update_me(user_service, user):
    update_data = UserUpdate(email="test@test.com", hashed_password="newpassword")
    result = await user_service.update_me(user, update_data)
    assert isinstance(result, UserRead)
    assert result.id == user.id
    assert result.email == update_data.email
