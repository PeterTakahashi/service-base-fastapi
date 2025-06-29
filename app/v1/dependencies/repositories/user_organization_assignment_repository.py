from app.v1.repositories.user_organization_assignment_repository import (
    UserOrganizationAssignmentRepository,
)
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session


def get_user_organization_assignment_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserOrganizationAssignmentRepository:
    return UserOrganizationAssignmentRepository(session)
