from sqladmin import ModelView
from app.models.user_api_key import UserApiKey


class UserApiKeyAdmin(ModelView, model=UserApiKey):
    name = "User Api Key"
    name_plural = "User Api Keys"

    icon = "fa-solid fa-key"

    column_list = [
        "id",
        "user_id",
        "prefix",
        "hashed_key",
        "deleted_at",
        "created_at",
        "user",
    ]

    form_columns = [
        "user_id",
    ]
