import pytest

from httpx import AsyncClient
from app.v1.schemas.organization import OrganizationCreate


@pytest.mark.asyncio
async def test_create_organization(auth_client: AsyncClient, user, fake_address):
    # Arrange
    organization_data = OrganizationCreate(
        name="Test Organization",
        description="A test organization",
        profile_image_key="test_profile_image_key",
        billing_email="test@test.com",
        address=fake_address,
        tax_type="eu_vat",
        tax_id="123456789",
    )
    response = await auth_client.post(
        "/organizations", json=organization_data.model_dump()
    )
    # Assert
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == organization_data.name
    assert response_data["description"] == organization_data.description
    assert response_data["profile_image_key"] == organization_data.profile_image_key
    assert response_data["billing_email"] == organization_data.billing_email
    assert response_data["created_by_user"]["id"] == str(user.id)
    assert response_data["address"]["city"] == organization_data.address.city
    assert response_data["address"]["country"] == organization_data.address.country
    assert response_data["address"]["line1"] == organization_data.address.line1
    assert response_data["address"]["line2"] == organization_data.address.line2
    assert response_data["address"]["postal_code"] == organization_data.address.postal_code
    assert response_data["address"]["state"] == organization_data.address.state
    assert response_data["tax_type"] == organization_data.tax_type
    assert response_data["tax_id"] == organization_data.tax_id
