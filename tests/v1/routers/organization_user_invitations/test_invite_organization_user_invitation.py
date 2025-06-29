import pytest

from httpx import AsyncClient
from app.v1.schemas.organization.invite import (
    OrganizationUserInvite,
)
from app.lib.utils.convert_id import encode_id
from tests.common.check_error_response import check_api_exception_response
from app.lib.error_code import ErrorCode
from fastapi import status


@pytest.mark.asyncio
async def test_invite_organization_user_invitation(
    auth_client: AsyncClient,
    organization,
    other_user,
    user_organization_invitation_repository,
):
    params = OrganizationUserInvite(
        email=other_user.email,
    )
    response = await auth_client.post(
        f"/organizations/{encode_id(organization.id)}/invite", json=params.model_dump()
    )
    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data is None
    # Check if the invitation was created in the repository
    invitation = await user_organization_invitation_repository.find_by(
        user_id=other_user.id,
        organization_id=organization.id,
    )
    assert invitation is not None
    assert invitation.user_id == other_user.id
    assert invitation.organization_id == organization.id


@pytest.mark.asyncio
async def test_invite_organization_user_invitation_not_found_organization(
    auth_client: AsyncClient,
    fake_id,
):
    params = OrganizationUserInvite(
        email="user@example.com",
    )
    response = await auth_client.post(
        f"/organizations/{fake_id}/invite", json=params.model_dump()
    )
    # Assert
    assert response.status_code == 404
    check_api_exception_response(
        response,
        status_code=status.HTTP_404_NOT_FOUND,
        detail_code=ErrorCode.NOT_FOUND,
    )
