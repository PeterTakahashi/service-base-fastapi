import pytest
from app.v1.schemas.organization import OrganizationCreate, OrganizationRead


@pytest.mark.asyncio
async def test_create_organization(
    organization_service,
    organization_repository,
    user_organization_assignment_repository,
    user,
    fake_address,
):
    # Arrange
    organization_data = OrganizationCreate(
        name="Test Organization",
        description="A test organization",
        profile_image_key="test_profile_image_key",
        billing_email="test@test.com",
        address=fake_address,
    )

    # Act
    created_organization = await organization_service.create(
        organization_data, user=user
    )

    # Assert
    assert isinstance(created_organization, OrganizationRead)
    assert created_organization.name == organization_data.name
    assert created_organization.description == organization_data.description
    assert created_organization.profile_image_key == organization_data.profile_image_key
    assert created_organization.billing_email == organization_data.billing_email

    # Verify that the organization was saved in the repository
    saved_organization = await organization_repository.find(created_organization.id)
    assert saved_organization is not None
    assert saved_organization.name == organization_data.name
    assert saved_organization.description == organization_data.description
    user_organization_assignment = (
        await user_organization_assignment_repository.find_by(
            user_id=user.id, organization_id=saved_organization.id
        )
    )
    assert user_organization_assignment is not None
    assert user_organization_assignment.user_id == user.id
    assert user_organization_assignment.organization_id == saved_organization.id
