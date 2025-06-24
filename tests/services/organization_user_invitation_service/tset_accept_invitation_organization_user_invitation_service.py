import pytest
from app.lib.error_code import ErrorCode
from tests.common.check_api_exception_info import check_api_exception_info
from fastapi import status
from datetime import datetime, timedelta


async def test_accept_invitation_success(
    organization_user_invitation_service,
    user_organization_invitation_repository,
    user_organization_assignment_repository,
    organization,
    user,
    other_user,
):
    await organization_user_invitation_service.invite_user(
        user=user,
        organization=organization,
        user_email=other_user.email,
    )
    await organization_user_invitation_service.accept_invitation(
        organization=organization,
        user=other_user,
    )
    user_organization_assignment = (
        await user_organization_assignment_repository.find_by(
            user_id=other_user.id, organization_id=organization.id
        )
    )
    assert user_organization_assignment is not None
    assert user_organization_assignment.user_id == other_user.id
    assert user_organization_assignment.organization_id == organization.id


async def test_accept_invitation_already_assigned_user(
    organization_user_invitation_service,
    user_organization_invitation_repository,
    user_organization_assignment_repository,
    organization,
    user,
):
    await organization_user_invitation_service.invite_user(
        user=user,
        organization=organization,
        user_email=user.email,
    )
    result = await organization_user_invitation_service.accept_invitation(
        organization=organization,
        user=user,
    )
    assert result is None
    user_organization_assignment = (
        await user_organization_assignment_repository.find_by(
            user_id=user.id, organization_id=organization.id
        )
    )
    assert user_organization_assignment is not None
    assert user_organization_assignment.user_id == user.id
    assert user_organization_assignment.organization_id == organization.id


async def test_accept_invitation_invalid_invitation(
    organization_user_invitation_service,
    user_organization_invitation_repository,
    user_organization_assignment_repository,
    organization,
    other_user,
):
    with pytest.raises(Exception) as exc_info:
        await organization_user_invitation_service.accept_invitation(
            organization=organization,
            user=other_user,
        )
    check_api_exception_info(
        exc_info,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail_code=ErrorCode.USER_ORGANIZATION_INVITATION_NOT_FOUND,
    )
    result = await user_organization_invitation_repository.find_by(
        user_id=other_user.id, organization_id=organization.id
    )
    assert result is None


async def test_accept_invitation_expired_invitation(
    organization_user_invitation_service,
    user_organization_invitation_repository,
    user_organization_assignment_repository,
    organization,
    other_user,
):
    # Simulate an expired invitation by creating one manually
    await user_organization_invitation_repository.create(
        user_id=other_user.id,
        organization_id=organization.id,
        created_by_user_id=other_user.id,
        created_at=datetime.utcnow() - timedelta(days=2),  # Expired invitation
    )

    with pytest.raises(Exception) as exc_info:
        await organization_user_invitation_service.accept_invitation(
            organization=organization,
            user=other_user,
        )
    check_api_exception_info(
        exc_info,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail_code=ErrorCode.USER_ORGANIZATION_INVITATION_EXPIRED,
    )
    result = await user_organization_invitation_repository.find_by(
        user_id=other_user.id, organization_id=organization.id
    )
    assert result is not None  # Invitation still exists but is expired


async def test_accept_invitation_already_assigned_user_invitation(
    organization_user_invitation_service,
    user_organization_invitation_repository,
    user_organization_assignment_repository,
    organization,
    user,
    other_user,
):
    # Create an invitation first
    await organization_user_invitation_service.invite_user(
        user=user,
        organization=organization,
        user_email=other_user.email,
    )
    await organization_user_invitation_service.accept_invitation(
        organization=organization,
        user=other_user,
    )
    # delete the assignment to simulate the user being invited again
    user_organization_assignment = (
        await user_organization_assignment_repository.find_by(
            user_id=other_user.id, organization_id=organization.id
        )
    )
    await user_organization_assignment_repository.destroy(
        user_organization_assignment.id
    )
    user_organization_assignment = (
        await user_organization_assignment_repository.find_by(
            user_id=other_user.id, organization_id=organization.id
        )
    )
    assert user_organization_assignment is None
    # Accept the invitation
    with pytest.raises(Exception) as exc_info:
        await organization_user_invitation_service.accept_invitation(
            organization=organization,
            user=other_user,
        )
    check_api_exception_info(
        exc_info,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail_code=ErrorCode.USER_ORGANIZATION_INVITATION_ALREADY_ASSIGNED,
    )
