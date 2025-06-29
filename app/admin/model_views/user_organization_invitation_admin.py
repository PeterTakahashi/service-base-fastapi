from sqladmin import ModelView
from app.models.user_organization_invitation import UserOrganizationInvitation


class UserOrganizationInvitationAdmin(ModelView, model=UserOrganizationInvitation):
    name = "User Organization Invitation"
    name_plural = "User Organization Invitations"

    icon = "fa-solid fa-envelope-open-text"

    column_list = [
        "id",
        "user_id",
        "organization_id",
        "email",
        "token",
        "is_accepted",
        "created_at",
        "user",
        "organization",
        "created_by_user",
    ]

    form_columns = [
        "user_id",
        "organization_id",
        "email",
        "token",
        "is_accepted",
    ]
