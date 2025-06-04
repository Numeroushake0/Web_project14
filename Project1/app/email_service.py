from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
from typing import Any

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_USER,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

fm = FastMail(conf)

async def send_verification_email(email: str, user_id: int) -> None:
    verify_link = f"http://localhost:8000/auth/verify-email?user_id={user_id}"
    message = MessageSchema(
        subject="Email verification",
        recipients=[email],
        body=f"Please verify your email by clicking on the following link: {verify_link}",
        subtype="plain",
    )
    await fm.send_message(message)

async def send_reset_password_email(email: str, user_id: int) -> None:
    reset_link = f"http://localhost:8000/auth/reset-password?user_id={user_id}"
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=f"To reset your password, click the following link: {reset_link}",
        subtype="plain",
    )
    await fm.send_message(message)
