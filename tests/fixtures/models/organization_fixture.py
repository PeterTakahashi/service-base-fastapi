import pytest_asyncio
from datetime import datetime

@pytest_asyncio.fixture
async def organization(
    organization_factory, user_organization_assignment_factory, user, organization_address_factory
):
    organization = await organization_factory.create(
        created_by_user_id=user.id,
    )
    await organization_address_factory.create(organization_id=organization.id)
    await user_organization_assignment_factory.create(
        user_id=user.id,
        organization_id=organization.id,
    )
    return organization


@pytest_asyncio.fixture
async def other_organization(
    organization_factory, user_organization_assignment_factory, other_user, organization_address_factory
):
    organization = await organization_factory.create(
        created_by_user_id=other_user.id,
    )
    await organization_address_factory.create(organization_id=organization.id)
    await user_organization_assignment_factory.create(
        user_id=other_user.id,
        organization_id=organization.id,
    )
    return organization


@pytest_asyncio.fixture
async def organization_with_users(
    organization, user_organization_assignment_factory, users, user_address_factory
):
    for user in users:
        await user_organization_assignment_factory.create(
            user_id=user.id,
            organization_id=organization.id,
        )
    return organization


@pytest_asyncio.fixture
async def soft_deleted_organization(
    organization_factory, user_organization_assignment_factory, user, organization_address_factory
):
    organization = await organization_factory.create(
        created_by_user_id=user.id,
        deleted_at=datetime.utcnow(),
    )
    await organization_address_factory.create(organization_id=organization.id)
    await user_organization_assignment_factory.create(
        user_id=user.id,
        organization_id=organization.id,
        deleted_at=datetime.utcnow(),
    )
    return organization


@pytest_asyncio.fixture
async def organizations(
    organization_factory, user_organization_assignment_factory, user, organization_address_factory
):
    organizations = await organization_factory.create_batch(
        5,
        created_by_user_id=user.id,
    )
    for organization in organizations:
        await user_organization_assignment_factory.create(
            user_id=user.id,
            organization_id=organization.id,
        )
        await organization_address_factory.create(organization_id=organization.id)
    return organizations
