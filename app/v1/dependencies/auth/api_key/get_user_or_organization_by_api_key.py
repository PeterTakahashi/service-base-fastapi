from app.lib.exception.api_exception import init_api_exception
from app.lib.error_code import ErrorCode

from fastapi import Depends, status
from app.models.user import User
from app.models.organization import Organization

from .get_organization_by_api_key import get_organization_by_api_key
from .get_user_by_api_key import get_user_by_api_key


def get_user_or_organization_by_api_key(
    user: User = Depends(get_user_by_api_key),
    organization: Organization = Depends(get_organization_by_api_key),
) -> User | Organization:
    """
    Dependency to get either a User or an Organization based on the API key.
    If both are found, it returns the User.
    If only the Organization is found, it returns the Organization.
    If neither is found, it raises an HTTP 401 Unauthorized error.
    """
    if user:
        return user
    elif organization:
        return organization
    else:
        raise init_api_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail_code=ErrorCode.UNAUTHORIZED_API_KEY,
        )
