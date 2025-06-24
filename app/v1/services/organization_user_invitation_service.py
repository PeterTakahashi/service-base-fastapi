from app.models.user import User
from app.models.organization import Organization
from app.v1.repositories.organization_repository import OrganizationRepository
from app.v1.repositories.user_organization_assignment_repository import (
    UserOrganizationAssignmentRepository,
)
from app.v1.repositories.user_organization_invitation_repository import (
    UserOrganizationInvitationRepository,
)
from app.v1.repositories.user_repository import UserRepository
from datetime import datetime, timedelta, timezone
from app.lib.error_code import ErrorCode

from fastapi_mail import FastMail
from fastapi_mail import MessageSchema, MessageType
from fastapi import status

from app.core.config import settings
from app.lib.exception.api_exception import init_api_exception


class OrganizationUserInvitationService:
    def __init__(
        self,
        organization_repository: OrganizationRepository,
        user_organization_assignment_repository: UserOrganizationAssignmentRepository,
        user_organization_invitation_repository: UserOrganizationInvitationRepository,
        user_repository: UserRepository,
        fast_mail: FastMail,
    ):
        self.organization_repository = organization_repository
        self.user_organization_assignment_repository = (
            user_organization_assignment_repository
        )
        self.user_organization_invitation_repository = (
            user_organization_invitation_repository
        )
        self.user_repository = user_repository
        self.fast_mail = fast_mail

    async def invite_user(
        self,
        user: User,
        organization: Organization,
        user_email: str,
    ) -> None:
        user = await self.user_repository.find_by(email=user_email)
        if not user:
            return None

        user_organization_assignment = (
            await self.user_organization_assignment_repository.find_by(
                user_id=user.id, organization_id=organization.id
            )
        )
        if user_organization_assignment:
            return None

        # create invitation
        await self.user_organization_invitation_repository.create(
            user_id=user.id,
            organization_id=organization.id,
            created_by_user_id=user.id,
        )
        await self.__send_invitation_email(organization, user_email)
        return None

    async def accept_invitation(
        self,
        organization: Organization,
        user: User,
    ) -> None:
        # return if user already assigned
        user_organization_assignment = (
            await self.user_organization_assignment_repository.find_by(
                user_id=user.id, organization_id=organization.id
            )
        )
        if user_organization_assignment:
            raise init_api_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.USER_ORGANIZATION_INVITATION_ALREADY_ASSIGNED,
            )

        # invalid if invitation not found
        user_organization_invitation = (
            await self.user_organization_invitation_repository.find_by(
                user_id=user.id, organization_id=organization.id
            )
        )
        if not user_organization_invitation:
            raise init_api_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.USER_ORGANIZATION_INVITATION_NOT_FOUND,
            )
        # invalid if expired
        if user_organization_invitation.created_at + timedelta(days=1) < datetime.now(
            timezone.utc
        ):
            raise init_api_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail_code=ErrorCode.USER_ORGANIZATION_INVITATION_EXPIRED,
            )
        # create user organization assignment
        await self.user_organization_assignment_repository.create(
            user_id=user.id,
            organization_id=organization.id,
        )
        await self.user_organization_invitation_repository.destroy(
            user_organization_invitation.id,
        )
        return None

    async def __send_invitation_email(
        self,
        organization: Organization,
        user_email: str,
    ):
        url = f"{settings.FRONTEND_URL}/organizations/{organization.id}/users/accept-invite"
        message = MessageSchema(
            subject="You have been invited to join an organization",
            recipients=[user_email],
            template_body={"url": url, "organization_name": organization.name},
            subtype=MessageType.html,
        )
        await self.fast_mail.send_message(
            message, template_name="email/invitation_organization.html"
        )
