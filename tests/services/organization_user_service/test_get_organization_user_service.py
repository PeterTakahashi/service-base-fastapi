import pytest
from app.v1.schemas.user.read import UserRead


@pytest.mark.asyncio
async def test_get_user_organization_user_service(
    organization_user_service, organization, user
):
    """
    Test the get_list method of OrganizationService.
    """
    # Call the service method
    response = await organization_user_service.get(
        organization_id=organization.id,
        user_id=user.id,
    )
    # Assert the response type
    assert isinstance(response, UserRead)
    # Assert the response data
    assert response.id == user.id
    assert response.email == user.email
