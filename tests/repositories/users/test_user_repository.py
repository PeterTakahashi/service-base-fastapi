import pytest_asyncio
from app.v1.repositories.user_repository import UserRepository


@pytest_asyncio.fixture
async def user_repository(async_session):
    return UserRepository(async_session)


async def test_update_user_success(user_repository, user):
    update_data = {"email": "new@example.com", "hashed_password": "newpassword"}

    updated_user = await user_repository.update_user(user, update_data)

    assert updated_user.email == "new@example.com"
    assert updated_user.hashed_password == "newpassword"
