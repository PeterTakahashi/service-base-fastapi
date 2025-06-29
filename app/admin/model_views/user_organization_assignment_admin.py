from sqladmin import ModelView
from app.models.user_organization_assignment import UserOrganizationAssignment


class UserOrganizationAssignmentAdmin(ModelView, model=UserOrganizationAssignment):
    name = "User Organization Assignment"
    name_plural = "User Organization Assignments"

    icon = "fa-solid fa-user-tag"

    column_list = [
        "id",
        "user_id",
        "organization_id",
        "role",
        "created_at",
        "user",
        "organization",
    ]

    form_columns = [
        "user_id",
        "organization_id",
        "role",
    ]
