import smtplib
from email.message import EmailMessage
from celery import Celery
from core.config import settings


celery = Celery("tasks", broker=f"redis://{settings.redis.host}:{settings.redis.port}")
celery.conf.broker_connection_retry_on_startup = True


def create_email(subject: str, content: str, email_address: str) -> EmailMessage:
    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = settings.smtp.user
    email["To"] = email_address
    email.set_content(content, subtype="html")
    return email


def get_email_template(token: str, email_type: str):
    if email_type == "verification":
        return (
            "<div>"
            f'<h1 style="color: black;">Здравствуйте, а вот и ваш код: {token}. 😊</h1>'
            "</div>"
        )
    elif email_type == "password_reset":
        return (
            "<div>"
            f'<h1 style="color: black;">Здравствуйте, а вот и ваш код для восстановления пароля: {token}. 😊</h1>'
            "</div>"
        )


@celery.task
def send_email(token: str, email_address: str, email_type: str):
    subject_map = {
        "verification": "Подтверждение почты Pastebin",
        "password_reset": "Восстановление пароля Pastebin",
    }
    subject = subject_map.get(email_type)
    content = get_email_template(token, email_type)
    email = create_email(subject, content, email_address)
    with smtplib.SMTP_SSL(settings.smtp.host, settings.smtp.port) as server:
        server.login(settings.smtp.user, settings.smtp.password)
        server.send_message(email)
