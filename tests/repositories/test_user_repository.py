import pytest
from unittest.mock import AsyncMock
from app.repositories.user_repository import UserRepository
from app.models.user import User
from uuid import uuid4

pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def user_repository(mock_session):
    return UserRepository(session=mock_session)

@pytest.fixture
def sample_user():
    user = User(id=uuid4(), email="old@example.com", hashed_password="oldpassword")
    return user

async def test_update_user_success(user_repository, mock_session, sample_user):
    update_data = {"email": "new@example.com", "hashed_password": "newpassword"}

    updated_user = await user_repository.update_user(sample_user, update_data)

    assert updated_user.email == "new@example.com"
    assert updated_user.hashed_password == "newpassword"
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(sample_user)
