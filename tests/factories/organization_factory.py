from app.models.organization import Organization
from tests.factories.async_factory import AsyncSQLAlchemyModelFactory

import factory
import pytest_asyncio


class OrganizationFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker("company")
    description = factory.Faker("text", max_nb_chars=200)
    billing_email = factory.Faker("email")
    profile_image_key = factory.Faker("file_name", extension="jpg")


@pytest_asyncio.fixture
async def organization_factory(async_session):
    OrganizationFactory._meta.session = async_session
    return OrganizationFactory
