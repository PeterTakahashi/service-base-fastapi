import pytest
from app.lib.error_code import ErrorCode
from tests.common.check_api_exception_info import check_api_exception_info
from fastapi import status


@pytest.mark.asyncio
async def test_delete_user_organization_user_service(
    organization_user_service,
    organization_with_users,
    user,
    user_organization_assignment_repository,
):
    """
    Test the get_list method of OrganizationService.
    """
    organization = organization_with_users
    # Call the service method
    response = await organization_user_service.delete(
        organization_id=organization.id,
        user_id=user.id,
    )
    # Assert the response type
    assert response is None
    # Assert the user is soft deleted
    user_organization_assignment = (
        await user_organization_assignment_repository.find_by(
            organization_id=organization.id,
            user_id=user.id,
            disable_default_scope=True,
        )
    )
    assert user_organization_assignment.deleted_at is not None


@pytest.mark.asyncio
async def test_delete_user_organization_user_service_last_one_user(
    organization_user_service,
    organization,
    user,
    user_organization_assignment_repository,
):
    """
    Test the get_list method of OrganizationService.
    """
    # Call the service method
    with pytest.raises(Exception) as exc_info:
        await organization_user_service.delete(
            organization_id=organization.id,
            user_id=user.id,
        )
    check_api_exception_info(
        exc_info,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail_code=ErrorCode.ORGANIZATION_LAST_USER_CANNOT_BE_DELETED,
    )
    user_organization_assignment = (
        await user_organization_assignment_repository.find_by(
            organization_id=organization.id,
            user_id=user.id,
        )
    )
    assert user_organization_assignment.deleted_at is None
