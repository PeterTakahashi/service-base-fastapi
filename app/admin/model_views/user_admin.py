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
    ]

    form_columns = [
        "email",
        "failed_attempts",
        "is_locked",
        "locked_until",
        "is_superuser",
    ]
