from app.models.user_organization_assignment import UserOrganizationAssignment
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory
import pytest_asyncio
import factory

from tests.factories.organization_factory import OrganizationFactory
from tests.factories.user_factory import UserFactory


class UserOrganizationAssignmentFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = UserOrganizationAssignment

    user = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)


@pytest_asyncio.fixture
async def user_organization_assignment_factory(async_session):
    UserOrganizationAssignmentFactory._meta.session = async_session
    return UserOrganizationAssignmentFactory
