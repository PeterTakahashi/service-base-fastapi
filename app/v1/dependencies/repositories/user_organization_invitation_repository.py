from app.v1.repositories.user_organization_invitation_repository import (
    UserOrganizationInvitationRepository,
)
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session


def get_user_organization_invitation_repository(
    session: AsyncSession = Depends(get_async_session),
) -> UserOrganizationInvitationRepository:
    return UserOrganizationInvitationRepository(session)
