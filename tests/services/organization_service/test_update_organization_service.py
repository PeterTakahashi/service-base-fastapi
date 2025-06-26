import pytest
from app.v1.schemas.organization import OrganizationUpdate, OrganizationRead
from app.v1.schemas.common.address.read import AddressRead

@pytest.mark.asyncio
async def test_update_organization_service(
    organization_service, organization_repository, organization, fake_address
):
    # Arrange
    update_data = OrganizationUpdate(
        name="Updated Organization Name",
        description="A test organization",
        profile_image_key="test_profile_image_key",
        billing_email="test@test.com",
        address=fake_address
    )

    # Act
    updated_organization = await organization_service.update(
        id=organization.id, organization_params=update_data
    )

    # Verify that the returned object is an instance of OrganizationRead
    assert isinstance(updated_organization, OrganizationRead)

    # Assert the updated fields
    assert updated_organization.name == update_data.name
    assert updated_organization.description == update_data.description
    assert updated_organization.profile_image_key == update_data.profile_image_key
    assert updated_organization.billing_email == update_data.billing_email
