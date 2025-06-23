import pytest
from app.v1.schemas.organization import OrganizationListRead, OrganizationSearchParams


@pytest.mark.asyncio
async def test_get_list_organization_service(organization_service, organizations, user):
    """
    Test the get_list method of OrganizationService.
    """
    # Call the service method
    response = await organization_service.get_list(
        user_id=user.id, search_params=OrganizationSearchParams()
    )

    # Assert the response is of type OrganizationListRead
    assert isinstance(response, OrganizationListRead)

    # Assert the response contains the expected number of organizations
    assert len(response.data) == len(organizations)

    # Assert that each organization in the response matches the expected data
    for org, expected_org in zip(response.data, organizations):
        assert org.id == expected_org.id
        assert org.name == expected_org.name


@pytest.mark.asyncio
async def test_get_list_organization_service_with_search_params(
    organization_service, organizations, user
):
    """
    Test the get_list method with search parameters.
    """
    search_params = OrganizationSearchParams(
        limit=10,
        offset=0,
        sorted_by="name",
        sorted_order="asc",
        name__icontains=organizations[0].name[
            :3
        ],  # Assuming the first org's name starts with 'Test'
    )

    response = await organization_service.get_list(
        user_id=user.id, search_params=search_params
    )

    assert isinstance(response, OrganizationListRead)
    assert len(response.data) > 0
