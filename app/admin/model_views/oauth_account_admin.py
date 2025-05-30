from sqladmin import ModelView
from app.db.session import engine
from app.models.oauth_account import OAuthAccount

class OAuthAccountAdmin(ModelView, model=OAuthAccount):
    name = "OAuthAccount"
    name_plural = "OAuthAccounts"

    icon = "fa-solid fa-plug"

    column_list = [
        "id",
        "user_id",
        "oauth_name",
        "access_token",
        "expires_at",
        "refresh_token",
        "account_id",
        "account_email"
    ]
    form_columns = [
        "user_id",
        "oauth_name",
        "access_token",
        "expires_at",
        "refresh_token",
        "account_id",
        "account_email"
    ]
    column_searchable_list = [
        "oauth_name",
        "account_email"
    ]
    column_filters = [
        "oauth_name",
        "account_email"
    ]