from tests.common.mailer import (
    get_latest_mail_source_by_recipient,
    get_subject_from_email_source,
)


async def test_invite_success(
    organization_user_invitation_service,
    user_organization_invitation_repository,
    organization,
    user,
    other_user,
):
    await organization_user_invitation_service.invite_user(
        user=user,
        organization=organization,
        user_email=other_user.email,
    )
    email_source = get_latest_mail_source_by_recipient(other_user.email)
    assert email_source is not None
    assert (
        get_subject_from_email_source(email_source)
        == "You have been invited to join an organization"
    )
    user_organization_invitation = (
        await user_organization_invitation_repository.find_by(
            user_id=other_user.id, organization_id=organization.id
        )
    )
    assert user_organization_invitation is not None


async def test_invite_not_found_user(
    organization_user_invitation_service,
    user_organization_invitation_repository,
    organization,
    user,
    faker,
):
    result = await organization_user_invitation_service.invite_user(
        user=user, organization=organization, user_email=faker.email()
    )
    assert result is None
    user_organization_invitation_repository = (
        await user_organization_invitation_repository.find_by(
            user_id=user.id, organization_id=organization.id
        )
    )
    assert user_organization_invitation_repository is None


async def test_invite_already_assigned_user(
    organization_user_invitation_service,
    user_organization_invitation_repository,
    organization,
    user,
):
    result = await organization_user_invitation_service.invite_user(
        user=user, organization=organization, user_email=user.email
    )
    assert result is None
    user_organization_invitation = (
        await user_organization_invitation_repository.find_by(
            user_id=user.id, organization_id=organization.id
        )
    )
    assert user_organization_invitation is None


async def test_invite_already_invited_user(
    organization_user_invitation_service,
    user_organization_invitation_repository,
    organization,
    user,
    other_user,
):
    await organization_user_invitation_service.invite_user(
        user=user,
        organization=organization,
        user_email=other_user.email,
    )
    result = await organization_user_invitation_service.invite_user(
        user=user,
        organization=organization,
        user_email=other_user.email,
    )
    assert result is None
    user_organization_invitations = await user_organization_invitation_repository.where(
        user_id=other_user.id, organization_id=organization.id
    )
    assert len(user_organization_invitations) == 2
