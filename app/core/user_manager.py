"""
This module defines the UserManager class and utility functions for managing user-related operations.
"""

from uuid import UUID  # Standard library imports
from typing import Union

from fastapi import Depends  # Third-party imports
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users import BaseUserManager, UUIDIDMixin, schemas, exceptions, models

from app.models.user import User  # First-party imports
from app.core.config import settings
from app.db.session import get_async_session


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    """
    UserManager handles user-related operations such as password validation
    and token management.
    """
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def validate_password(
        self, password: str, user: Union[schemas.UC, models.UP]
    ) -> None:
        """
        Validates the given password against security requirements.

        Args:
            password (str): The password to validate.
            user (Union[schemas.UC, models.UP]): The user object.

        Raises:
            InvalidPasswordException: If the password does not meet the requirements.
        """
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


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Dependency function to get the user database.

    Args:
        session (AsyncSession): The database session.

    Yields:
        SQLAlchemyUserDatabase: The user database instance.
    """
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Dependency function to get the user manager.

    Args:
        user_db: The user database dependency.

    Yields:
        UserManager: The user manager instance.
    """
    yield UserManager(user_db)