import pytest

from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_list_organization(auth_client: AsyncClient, organization):
    response = await auth_client.get("/organizations")
    # Assert
    assert response.status_code == 200
    response_data = response.json()["data"]
    assert isinstance(response_data, list)
    assert len(response_data) > 0

    # Check if the first organization matches the expected structure
    first_org = response_data[0]
    assert "id" in first_org
    assert "name" in first_org
    assert "description" in first_org
    assert "profile_image_key" in first_org
    assert "billing_email" in first_org
