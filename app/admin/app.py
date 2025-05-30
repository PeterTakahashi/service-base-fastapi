from sqladmin import Admin
from app.db.session import engine
from app.admin.admin_auth import AdminAuth

from app.admin.model_views.user_admin import UserAdmin
from app.admin.model_views.wallet_admin import WalletAdmin
from app.admin.model_views.wallet_transaction_admin import WalletTransactionAdmin
from app.admin.model_views.oauth_account_admin import OAuthAccountAdmin

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
    admin.add_view(WalletAdmin)
    admin.add_view(WalletTransactionAdmin)
    admin.add_view(OAuthAccountAdmin)
    return app