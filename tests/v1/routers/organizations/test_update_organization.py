import pytest
import pytest_asyncio

from httpx import AsyncClient
from app.v1.schemas.organization import OrganizationUpdate
from app.lib.utils.convert_id import encode_id
from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode
from fastapi import status


@pytest_asyncio.fixture
def updated_data(fake_address):
    return OrganizationUpdate(
        name="Updated Organization",
        description="An updated organization",
        profile_image_key="updated_profile_image_key",
        billing_email="test@test.com",
        address=fake_address,
        tax_type="eu_vat",
        tax_id="123456789",
    )


@pytest.mark.asyncio
async def test_update_organization(
    auth_client: AsyncClient,
    organization,
    updated_data: OrganizationUpdate,
):
    response = await auth_client.patch(
        f"/organizations/{encode_id(organization.id)}", json=updated_data.model_dump()
    )
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == updated_data.name
    assert response_data["description"] == updated_data.description
    assert response_data["profile_image_key"] == updated_data.profile_image_key
    assert response_data["billing_email"] == updated_data.billing_email
    assert response_data["address"]["city"] == updated_data.address.city
    assert response_data["address"]["country"] == updated_data.address.country
    assert response_data["address"]["line1"] == updated_data.address.line1
    assert response_data["address"]["line2"] == updated_data.address.line2
    assert response_data["address"]["postal_code"] == updated_data.address.postal_code
    assert response_data["address"]["state"] == updated_data.address.state
    assert response_data["tax_type"] == updated_data.tax_type
    assert response_data["tax_id"] == updated_data.tax_id


@pytest.mark.asyncio
async def test_update_by_other_user(
    other_auth_client: AsyncClient,
    organization,
    updated_data: OrganizationUpdate,
):
    response = await other_auth_client.patch(
        f"/organizations/{encode_id(organization.id)}", json=updated_data.model_dump()
    )
    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )


@pytest.mark.asyncio
async def test_update_uncreated_organization(
    auth_client: AsyncClient,
    fake_id,
    updated_data: OrganizationUpdate,
):
    response = await auth_client.patch(
        f"/organizations/{fake_id}", json=updated_data.model_dump()
    )
    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response, status_code=status.HTTP_404_NOT_FOUND, detail_code=ErrorCode.NOT_FOUND
    )
