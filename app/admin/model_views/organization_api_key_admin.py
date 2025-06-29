from sqladmin import ModelView
from app.models.organization_api_key import OrganizationApiKey


class OrganizationApiKeyAdmin(ModelView, model=OrganizationApiKey):
    name = "Organization Api Key"
    name_plural = "Organization Api Keys"

    icon = "fa-solid fa-key"

    column_list = [
        "id",
        "organization_id",
        "key_name",
        "prefix",
        "created_at",
        "organization",
        "created_by_user",
    ]

    form_columns = [
        "organization_id",
        "key_name",
    ]
