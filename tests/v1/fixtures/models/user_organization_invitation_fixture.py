import pytest_asyncio
from app.v1.schemas.organization.invite import (
    OrganizationUserInvite,
)
from app.lib.utils.convert_id import encode_id


@pytest_asyncio.fixture
async def user_organization_invitation(
    auth_client, organization, other_user, user_organization_invitation_repository
):
    params = OrganizationUserInvite(
        email=other_user.email,
    )
    await auth_client.post(
        f"/organizations/{encode_id(organization.id)}/invite", json=params.model_dump()
    )
    user_organization_invitation = (
        await user_organization_invitation_repository.find_by(
            user_id=other_user.id,
            organization_id=organization.id,
        )
    )
    return user_organization_invitation
