from app.models.user_organization_assignment import UserOrganizationAssignment
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import pytest_asyncio


class UserOrganizationAssignmentFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = UserOrganizationAssignment


@pytest_asyncio.fixture
async def user_organization_assignment_factory(async_session):
    UserOrganizationAssignmentFactory._meta.session = async_session
    return UserOrganizationAssignmentFactory
