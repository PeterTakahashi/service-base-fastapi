from enum import Enum


class ErrorCode(str, Enum):
    REGISTER_INVALID_PASSWORD = "register_invalid_password"
    REGISTER_USER_ALREADY_EXISTS = "register_user_already_exists"
    OAUTH_NOT_AVAILABLE_EMAIL = "oauth_not_available_email"
    OAUTH_USER_ALREADY_EXISTS = "oauth_user_already_exists"
    LOGIN_BAD_CREDENTIALS = "login_bad_credentials"
    LOGIN_USER_NOT_VERIFIED = "login_user_not_verified"
    RESET_PASSWORD_BAD_TOKEN = "reset_password_bad_token"
    RESET_PASSWORD_INVALID_PASSWORD = "reset_password_invalid_password"
    VERIFY_USER_BAD_TOKEN = "verify_user_bad_token"
    VERIFY_USER_ALREADY_VERIFIED = "verify_user_already_verified"
    UPDATE_USER_EMAIL_ALREADY_EXISTS = "update_user_email_already_exists"
    UPDATE_USER_INVALID_PASSWORD = "update_user_invalid_password"
    VALIDATION_ERROR = "validation_error"
