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
    INVALID_PAYLOAD = "invalid_payload"
    UNAUTHORIZED = "unauthorized"
    UNAUTHORIZED_API_KEY = "unauthorized_api_key"
    NOT_FOUND = "not_found"
    INVALID_IP = "invalid_ip"
    INVALID_ORIGIN = "invalid_origin"
    EXPIRED_API_KEY = "expired_api_key"
    LOGIN_ACCOUNT_LOCKED = "login_account_locked"
    INVALID_STATE_TOKEN = "invalid_state_token"
    INTERNAL_SERVER_ERROR = "internal_server_error"
    USER_ORGANIZATION_INVITATION_NOT_FOUND = "user_organization_invitation_not_found"
    USER_ORGANIZATION_INVITATION_EXPIRED = "user_organization_invitation_expired"
    USER_ORGANIZATION_INVITATION_ALREADY_ASSIGNED = (
        "user_organization_invitation_already_assigned"
    )
    ORGANIZATION_LAST_USER_CANNOT_BE_DELETED = (
        "organization_last_user_cannot_be_deleted"
    )
    FAILED_TO_CREATE_PAYMENT_INTENT = "failed_to_create_payment_intent"
    FAILED_TO_WEBHOOK_PAYMENT_INTENT_UPDATE = "failed_to_webhook_payment_intent_update"
