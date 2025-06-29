from sqladmin import ModelView
from app.models.organization import Organization


class OrganizationAdmin(ModelView, model=Organization):
    name = "Organization"
    name_plural = "Organizations"

    icon = "fa-solid fa-building"

    column_list = [
        "id",
        "name",
        "description",
        "billing_email",
        "tax_type",
        "tax_id",
        "created_by_user_id",
        "organization_wallet",
        "organization_api_keys",
        "address",
        "created_at",
        "updated_at",
        "deleted_at",
        "user_organization_assignments",
        "user_organization_invitations",
        "created_by_user",
    ]

    column_searchable_list = [
        "name",
        "description",
        "billing_email",
        "tax_id",
    ]

    column_sortable_list = [
        "id",
        "name",
        "created_at",
        "updated_at",
    ]

    form_columns = [
        "name",
        "description",
        "profile_image_key",
        "billing_email",
        "tax_type",
        "tax_id",
        "created_by_user_id",
    ]

    column_details_list = [
        "id",
        "name",
        "description",
        "profile_image_key",
        "billing_email",
        "tax_type",
        "tax_id",
        "created_by_user_id",
        "created_at",
        "updated_at",
        "deleted_at",
    ]
