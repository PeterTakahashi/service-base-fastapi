from fastapi_mail import FastMail
from app.lib.utils.mailer import mailer


def get_mailer() -> FastMail:
    return mailer
