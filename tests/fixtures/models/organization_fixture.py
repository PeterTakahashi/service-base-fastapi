import pytest_asyncio
from datetime import datetime


@pytest_asyncio.fixture
async def organization(
    organization_factory,
    organization_wallet_factory,
    user_organization_assignment_factory,
    user,
    organization_address_factory,
):
    organization = await organization_factory.create(
        created_by_user=user,
    )
    await organization_wallet_factory.create(organization=organization)
    await organization_address_factory.create(organization=organization)
    await user_organization_assignment_factory.create(
        user=user,
        organization=organization,
    )
    return organization


@pytest_asyncio.fixture
async def other_organization(
    organization_factory,
    user_organization_assignment_factory,
    other_user,
    organization_address_factory,
    organization_wallet_factory,
):
    organization = await organization_factory.create(
        created_by_user=other_user,
    )
    await organization_wallet_factory.create(organization=organization)
    await organization_address_factory.create(organization=organization)
    await user_organization_assignment_factory.create(
        user=other_user,
        organization=organization,
    )
    return organization


@pytest_asyncio.fixture
async def organization_with_users(
    organization, user_organization_assignment_factory, users
):
    for user in users:
        await user_organization_assignment_factory.create(
            user=user,
            organization=organization,
        )
    return organization


@pytest_asyncio.fixture
async def soft_deleted_organization(
    organization_factory,
    user_organization_assignment_factory,
    organization_wallet_factory,
    user,
    organization_address_factory,
):
    organization = await organization_factory.create(
        created_by_user=user,
        deleted_at=datetime.utcnow(),
    )
    await organization_wallet_factory.create(organization=organization)
    await organization_address_factory.create(organization=organization)
    await user_organization_assignment_factory.create(
        user=user,
        organization=organization,
        deleted_at=datetime.utcnow(),
    )
    return organization


@pytest_asyncio.fixture
async def organizations(
    organization_factory,
    user_organization_assignment_factory,
    user,
    organization_address_factory,
    organization_wallet_factory,
):
    organizations = await organization_factory.create_batch(
        5,
        created_by_user=user,
    )
    for organization in organizations:
        await user_organization_assignment_factory.create(
            user=user,
            organization=organization,
        )
        await organization_wallet_factory.create(organization=organization)
        await organization_address_factory.create(organization=organization)
    return organizations
