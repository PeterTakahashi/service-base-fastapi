"""
This module defines the UserManager class and utility functions for managing user-related operations.
"""

from uuid import UUID
from typing import Optional, Union
from datetime import datetime, timezone, timedelta

from fastapi import Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions, models, schemas
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.core.config import settings
from app.db.session import get_async_session
from app.core.mailer import mailer
from fastapi_mail import MessageSchema, MessageType

from app.models.user import User
from app.models.oauth_account import OAuthAccount


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    """
    UserManager handles user-related operations such as password validation
    and token management.
    """

    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    AUTHENTICATE_MAX_FAILED_ATTEMPTS = settings.AUTHENTICATE_MAX_FAILED_ATTEMPTS
    LOCK_MINUTES = 30
    RESET_FAILED_ATTEMPTS_SECONDS = 1800  # 30 minutes

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """
        Called after sending a request to verify the user's email.
        You can customize this method to send a verification email, etc.
        """
        url = f"{settings.FRONTEND_URL}/verify-token/{token}"
        message = MessageSchema(
            subject="Email Verification",
            recipients=[user.email],
            template_body={"url": url},
            subtype=MessageType.html,
        )
        await mailer.send_message(message, template_name="email/verify_email.html")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """
        Called after a user requests a forgot-password link.
        You can customize this method to send an email with reset instructions.
        """
        url = f"{settings.FRONTEND_URL}/reset-password/{token}"
        message = MessageSchema(
            subject="Password Reset Request",
            recipients=[user.email],
            template_body={"user_id": str(user.id), "url": url},
            subtype=MessageType.html,
        )
        await mailer.send_message(message, template_name="email/reset_password.html")

    async def validate_password(
        self, password: str, user: Union[schemas.UC, models.UP]
    ) -> None:
        """
        Validates the given password against security requirements.

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

    async def authenticate(  # type: ignore[override]
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:
        """
        Authenticates a user based on email + password credentials.
        If the login fails, increments the failed_attempts counter.
        When the failed attempts exceed a threshold, locks the account.
        If already locked, raises HTTP 423 or unlocks if enough time has passed.
        Returns None if authentication fails, or the user instance on success.
        """
        try:
            user = await self.get_by_email(credentials.username)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None
        # Check if the user is currently locked and possibly unlock
        if not await self._handle_lock_state(user):
            # Still locked
            raise HTTPException(status_code=423, detail="LOGIN_ACCOUNT_LOCKED")

        # Reset failed_attempts if enough time has passed since last attempt
        self._maybe_reset_failed_attempts(user)

        # Validate password
        verified, updated_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )

        if not verified:
            await self._increment_failed_attempts(user)
            return None

        # If the hash was updated, persist it
        if updated_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_hash})

        # Successful login => reset lock state
        await self._reset_failures_and_unlock(user)
        return user

    async def _handle_lock_state(self, user: User) -> bool:
        """
        If the user is locked and lock time has not passed, return False.
        If the user is locked but lock time has passed, unlock them.
        Otherwise, return True (user is not locked).
        """
        if not user.is_locked:
            return True

        # If locked_until is still in the future, user stays locked
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            return False

        # Otherwise, unlock (the lock time has passed)
        await self._reset_failures_and_unlock(user)
        return True

    def _maybe_reset_failed_attempts(self, user: User) -> None:
        """
        If the last failed login attempt was more than RESET_FAILED_ATTEMPTS_SECONDS ago,
        reset the failed_attempts counter to 0.
        """
        if user.last_attempted_at:
            elapsed = datetime.now(timezone.utc) - user.last_attempted_at
            if elapsed.total_seconds() > self.RESET_FAILED_ATTEMPTS_SECONDS:
                user.failed_attempts = 0

    async def _increment_failed_attempts(self, user: User) -> None:
        """
        Increment the failed_attempts count and set locked status if it reaches the threshold.
        """
        now = datetime.now(timezone.utc)
        user.failed_attempts += 1
        user.last_attempted_at = now

        if user.failed_attempts >= self.AUTHENTICATE_MAX_FAILED_ATTEMPTS:
            user.is_locked = True
            user.locked_until = now + timedelta(minutes=self.LOCK_MINUTES)

        await self.user_db.update(
            user,
            {
                "failed_attempts": user.failed_attempts,
                "last_attempted_at": user.last_attempted_at,
                "is_locked": user.is_locked,
                "locked_until": user.locked_until,
            },
        )

    async def _reset_failures_and_unlock(self, user: User) -> None:
        """
        Reset failed_attempts, clear lock flags, and update DB.
        """
        user.failed_attempts = 0
        user.is_locked = False
        user.locked_until = None
        user.last_attempted_at = None

        await self.user_db.update(
            user,
            {
                "failed_attempts": user.failed_attempts,
                "is_locked": user.is_locked,
                "locked_until": user.locked_until,
                "last_attempted_at": user.last_attempted_at,
            },
        )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Dependency function to retrieve the user database instance.

    Yields:
        SQLAlchemyUserDatabase: The user database instance.
    """
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Dependency function to retrieve the user manager instance.

    Args:
        user_db: The user database dependency.

    Yields:
        UserManager: The user manager instance.
    """
    yield UserManager(user_db)
