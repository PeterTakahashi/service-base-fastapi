from sqladmin import ModelView
from app.models.user_address import UserAddress


class UserAddressAdmin(ModelView, model=UserAddress):
    name = "User Address"
    name_plural = "User Addresses"

    icon = "fa-solid fa-location-dot"

    column_list = [
        "id",
        "user_id",
        "address_line_1",
        "address_line_2",
        "city",
        "state_province_region",
        "postal_code",
        "country",
        "created_at",
        "user",
    ]

    form_columns = [
        "user_id",
        "address_line_1",
        "address_line_2",
        "city",
        "state_province_region",
        "postal_code",
        "country",
    ]
