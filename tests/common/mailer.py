import base64
import re
from app.core.config import settings
import httpx


def email_decode(source: str) -> str:
    base64_body_match = re.search(
        r"Content-Transfer-Encoding: base64\s+([A-Za-z0-9+/=\n]+)--=", source, re.DOTALL
    )
    if not base64_body_match:
        raise ValueError("Base64 content not found")

    base64_body = base64_body_match.group(1).strip()
    decoded_bytes = base64.b64decode(base64_body)
    return decoded_bytes.decode("utf-8")


def get_password_reset_token_from_email_source(prefix: str, source: str) -> str:
    email_decoded = email_decode(source)
    token_match = re.search(rf"{re.escape(prefix)}([A-Za-z0-9\-._~]+)", email_decoded)
    if not token_match:
        raise ValueError("Token not found")
    return token_match.group(1)


def get_latest_mail_source_by_recipient(target_email: str) -> str:
    url = f"http://{settings.MAIL_SERVER}:{settings.MAIL_WEB_PORT}/api/messages/?page=1"
    response = httpx.get(url).json()

    for message in response.get("data", []):
        raw = message.get("raw", "")
        source = message.get("source", "")
        if target_email in raw or target_email in source:
            return source

    raise ValueError(f"No email found for recipient: {target_email}")
