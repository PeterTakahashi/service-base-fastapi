from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import BaseUserManager, UUIDIDMixin, schemas, exceptions, models
from app.db.models.user import User
from uuid import UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from fastapi import Depends
from typing import Union

# Reuse the same async engine and session
DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

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

async def get_user_db():
    async with async_session_maker() as session:
        yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
