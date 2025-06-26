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
