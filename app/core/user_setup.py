from fastapi_users import FastAPIUsers
from app.models.user import User
from app.core.auth import jwt_auth_backend, cookie_auth_backend
from app.core.user_manager import get_user_manager
from uuid import UUID

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [jwt_auth_backend, cookie_auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
