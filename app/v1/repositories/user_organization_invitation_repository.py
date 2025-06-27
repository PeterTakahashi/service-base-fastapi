from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_organization_invitation import UserOrganizationInvitation
from fastapi_repository import BaseRepository


class UserOrganizationInvitationRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserOrganizationInvitation)
