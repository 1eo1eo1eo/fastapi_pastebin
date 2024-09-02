import smtplib
from email.message import EmailMessage

from celery import Celery
from core.config import settings


celery = Celery("tasks", broker=f"redis://{settings.redis.host}:{settings.redis.port}")
celery.conf.broker_connection_retry_on_startup = True


def get_email_template_registration_verify(
    token: str,
    email_address: str,
):
    email = EmailMessage()
    email["Subject"] = "Подтверждение почты Pastebin"
    email["From"] = settings.smtp.user
    email["To"] = email_address

    email.set_content(
        "<div>"
        f'<h1 style="color: black;">Здравствуйте, а вот и ваш код: {token}. 😊</h1>'
        "-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app"
        '-mobile-free-vector.jpg" width="600">'
        "</div>",
        subtype="html",
    )
    return email


def get_email_template_password_reset(
    token: str,
    email_address: str,
):
    email = EmailMessage()
    email["Subject"] = "Восставновление пароля Pastebin"
    email["From"] = settings.smtp.user
    email["To"] = email_address

    email.set_content(
        "<div>"
        f'<h1 style="color: black;">Здравствуйте, а вот и ваш код для восставновления пароля: {token}. 😊</h1>'
        "</div>",
        subtype="html",
    )
    return email


@celery.task
def send_email_registration_verify_token(token: str, email_address: str):
    email = get_email_template_registration_verify(token, email_address)
    with smtplib.SMTP_SSL(settings.smtp.host, settings.smtp.port) as server:
        server.login(settings.smtp.user, settings.smtp.password)
        server.send_message(email)


@celery.task
def send_email_password_reset_token(token: str, email_address: str):
    email = get_email_template_password_reset(token, email_address)
    with smtplib.SMTP_SSL(settings.smtp.host, settings.smtp.port) as server:
        server.login(settings.smtp.user, settings.smtp.password)
        server.send_message(email)
