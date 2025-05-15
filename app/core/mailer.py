from fastapi_mail import FastMail, ConnectionConfig
from pathlib import Path
from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_FOLDER = Path(BASE_DIR / "templates")

mailer_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=TEMPLATE_FOLDER,
)
mailer = FastMail(mailer_config)
