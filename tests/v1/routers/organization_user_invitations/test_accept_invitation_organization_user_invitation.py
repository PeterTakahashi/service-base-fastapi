import pytest

from httpx import AsyncClient

from app.lib.utils.convert_id import encode_id
from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode
from fastapi import status


@pytest.mark.asyncio
async def test_accept_invitation_user_organization_invitation(
    other_auth_client: AsyncClient,
    user_organization_invitation,
    organization,
    other_user,
    user_organization_invitation_repository,
    user_organization_assignment_repository,
):
    response = await other_auth_client.patch(
        f"/organizations/{encode_id(organization.id)}/invite/accept",
    )
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data is None

    # Check if the invitation is assigned
    invitation = await user_organization_invitation_repository.find_by(
        user_id=other_user.id,
        organization_id=user_organization_invitation.organization_id,
    )
    assert invitation is None

    # Check if the user is assigned to the organization
    assignment = await user_organization_assignment_repository.find_by(
        user_id=other_user.id,
        organization_id=user_organization_invitation.organization_id,
    )
    assert assignment is not None


@pytest.mark.asyncio
async def test_accept_invitation_user_organization_invitation_not_found_organization(
    other_auth_client: AsyncClient,
    fake_id,
):
    response = await other_auth_client.patch(
        f"/organizations/{fake_id}/invite/accept",
    )
    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response,
        status_code=status.HTTP_404_NOT_FOUND,
        detail_code=ErrorCode.NOT_FOUND,
    )


@pytest.mark.asyncio
async def test_accept_invitation_user_organization_invitation_assigned(
    auth_client: AsyncClient,
    organization,
):
    response = await auth_client.patch(
        f"/organizations/{encode_id(organization.id)}/invite/accept",
    )
    # Assert
    assert response.status_code == 400
    check_api_exception_response(
        response,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail_code=ErrorCode.USER_ORGANIZATION_INVITATION_ALREADY_ASSIGNED,
    )
