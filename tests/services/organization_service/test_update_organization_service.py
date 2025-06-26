import pytest
from app.v1.schemas.organization import OrganizationUpdate, OrganizationRead


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
        address=fake_address,
        tax_type="eu_vat",
        tax_id="123456789",
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
    assert updated_organization.address.city == update_data.address.city
    assert updated_organization.address.country == update_data.address.country
    assert updated_organization.address.line1 == update_data.address.line1
    assert updated_organization.address.line2 == update_data.address.line2
    assert updated_organization.address.postal_code == update_data.address.postal_code
    assert updated_organization.address.state == update_data.address.state
    assert updated_organization.tax_type == update_data.tax_type
    assert updated_organization.tax_id == update_data.tax_id
