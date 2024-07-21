import smtplib

from pydantic import EmailStr

from app.config import SMTP_HOST, SMTP_PASS, SMTP_PORT, SMTP_USER
from app.tasks.email_templates import create_reset_pass_template


def send_reset_pass(
        email_to: EmailStr,
        code: str,
):
    msg_content = create_reset_pass_template(email_to, code)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg_content)
