from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import BaseUserManager, UUIDIDMixin, schemas, exceptions, models
from app.models.user import User
from uuid import UUID
from app.core.config import settings
from fastapi import Depends
from app.db.session import get_async_session
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession

class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def validate_password(
        self, password: str, user: Union[schemas.UC, models.UP]
    ) -> None:
        if len(password) < 8:
            raise exceptions.InvalidPasswordException(
                reason="Password must be at least 8 characters long"
            )
        if not any(char.isdigit() for char in password):
            raise exceptions.InvalidPasswordException(
                reason="Password must contain at least one digit"
            )
        if not any(char.isalpha() for char in password):
            raise exceptions.InvalidPasswordException(
                reason="Password must contain at least one letter"
            )
        if not any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in password):
            raise exceptions.InvalidPasswordException(
                reason="Password must contain at least one special character"
            )

async def get_user_db(session: AsyncSession = Depends(get_async_session)): # 依存性注入を使用
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
