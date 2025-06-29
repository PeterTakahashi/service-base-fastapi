from sqladmin import ModelView
from app.models.organization_address import OrganizationAddress


class OrganizationAddressAdmin(ModelView, model=OrganizationAddress):
    name = "Organization Address"
    name_plural = "Organization Addresses"

    icon = "fa-solid fa-location-dot"

    column_list = [
        "id",
        "organization_id",
        "address_line_1",
        "address_line_2",
        "city",
        "state_province_region",
        "postal_code",
        "country",
        "created_at",
        "organization",
    ]

    form_columns = [
        "organization_id",
        "address_line_1",
        "address_line_2",
        "city",
        "state_province_region",
        "postal_code",
        "country",
    ]
