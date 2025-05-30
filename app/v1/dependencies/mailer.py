from fastapi_mail import FastMail
from app.core.mailer import mailer


def get_mailer() -> FastMail:
    return mailer
