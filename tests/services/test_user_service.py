import pytest
from unittest.mock import AsyncMock
from app.services.user_service import UserService
from app.models.user import User
from app.schemas.user import UserUpdate
from uuid import uuid4

pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_user_repository():
    return AsyncMock()

@pytest.fixture
def user_service(mock_user_repository):
    return UserService(user_repository=mock_user_repository)

@pytest.fixture
def sample_user():
    return User(id=uuid4(), email="test@example.com", hashed_password="hashedpassword")

async def test_get_me(user_service, sample_user):
    result = await user_service.get_me(sample_user)

    assert result.id == sample_user.id
    assert result.email == sample_user.email

async def test_update_me_success(user_service, mock_user_repository, sample_user):
    update_data = UserUpdate(email="new@example.com")
    mock_user_repository.update_user.return_value = sample_user

    result = await user_service.update_me(sample_user, update_data)

    mock_user_repository.update_user.assert_called_once()
    assert result.id == sample_user.id
    assert result.email == sample_user.email
