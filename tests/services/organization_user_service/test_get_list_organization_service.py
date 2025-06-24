import pytest
from app.v1.schemas.organization.users.search_params import (
    OrganizationUserSearchParams,
)
from app.v1.schemas.common.list.base_list_response import ListResponseMeta
from app.v1.schemas.organization.users.read_list import UserListRead


@pytest.mark.asyncio
async def test_get_list_organization_user_service(
    organization_user_service, organization_with_users
):
    """
    Test the get_list method of OrganizationService.
    """
    # Call the service method
    response = await organization_user_service.get_list(
        organization_id=organization_with_users.id,
        search_params=OrganizationUserSearchParams(),
    )
    # Assert the response type
    assert isinstance(response, UserListRead)
    # Assert the response meta data
    assert isinstance(response.meta, ListResponseMeta)
    # Assert the response data is a list
    assert isinstance(response.data, list)
    # length
    assert len(response.data) == 11


@pytest.mark.asyncio
async def test_get_list_organization_user_service_limited(
    organization_user_service, organization_with_users
):
    """
    Test the get_list method of OrganizationService.
    """
    # Call the service method
    response = await organization_user_service.get_list(
        organization_id=organization_with_users.id,
        search_params=OrganizationUserSearchParams(
            limit=3,
            offset=0,
            sorted_by="email",
            sorted_order="asc",
        ),
    )
    # length
    assert len(response.data) == 3


@pytest.mark.asyncio
async def test_get_list_organization_user_service_filtered(
    organization_user_service, organization_with_users, user
):
    """
    Test the get_list method of OrganizationService with filters.
    """
    # Call the service method
    response = await organization_user_service.get_list(
        organization_id=organization_with_users.id,
        search_params=OrganizationUserSearchParams(
            email__icontains=user.email,
        ),
    )
    # Assert the response type
    assert isinstance(response, UserListRead)
    # Assert the response meta data
    assert isinstance(response.meta, ListResponseMeta)
    # Assert the response data is a list
    assert isinstance(response.data, list)
    # length
    assert len(response.data) == 1
