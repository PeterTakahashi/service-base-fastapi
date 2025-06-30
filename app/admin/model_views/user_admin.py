from sqladmin import ModelView
from app.models.user import User


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"

    icon = "fa-solid fa-user"

    column_list = [
        "id",
        "email",
        "failed_attempts",
        "is_locked",
        "locked_until",
        "is_superuser",
        "created_at",
        "oauth_accounts",
        "user_wallet",
        "user_api_keys",
        "user_organization_assignments",
        "user_organization_invitations",
        "address",
    ]

    form_columns = [
        "email",
        "failed_attempts",
        "is_locked",
        "locked_until",
        "is_superuser",
    ]
