from sqladmin import Admin
from app.db.session import engine
from app.admin.admin_auth import AdminAuth

from app.admin.model_views.user_admin import UserAdmin
from app.admin.model_views.user_wallet_admin import UserWalletAdmin
from app.admin.model_views.user_wallet_transaction_admin import (
    UserWalletTransactionAdmin,
)
from app.admin.model_views.oauth_account_admin import OAuthAccountAdmin
from app.admin.model_views.user_api_key_admin import UserApiKeyAdmin
from app.admin.model_views.organization_admin import OrganizationAdmin
from app.admin.model_views.organization_address_admin import (
    OrganizationAddressAdmin,
)
from app.admin.model_views.organization_api_key_admin import (
    OrganizationApiKeyAdmin,
)
from app.admin.model_views.organization_wallet_admin import (
    OrganizationWalletAdmin,
)
from app.admin.model_views.organization_wallet_transaction_admin import (
    OrganizationWalletTransactionAdmin,
)
from app.admin.model_views.user_address_admin import UserAddressAdmin
from app.admin.model_views.user_organization_assignment_admin import (
    UserOrganizationAssignmentAdmin,
)
from app.admin.model_views.user_organization_invitation_admin import (
    UserOrganizationInvitationAdmin,
)


def init_sqladmin(app):
    admin_auth = AdminAuth(secret_key="your-secret-key")
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=admin_auth,
        title="Admin",
        base_url="/admin",
    )
    admin.add_view(UserAdmin)
    admin.add_view(UserWalletAdmin)
    admin.add_view(UserWalletTransactionAdmin)
    admin.add_view(OAuthAccountAdmin)
    admin.add_view(UserApiKeyAdmin)
    admin.add_view(OrganizationAdmin)
    admin.add_view(OrganizationAddressAdmin)
    admin.add_view(OrganizationApiKeyAdmin)
    admin.add_view(OrganizationWalletAdmin)
    admin.add_view(OrganizationWalletTransactionAdmin)
    admin.add_view(UserAddressAdmin)
    admin.add_view(UserOrganizationAssignmentAdmin)
    admin.add_view(UserOrganizationInvitationAdmin)
    return app
