from email.message import EmailMessage
import os
import smtplib
import ssl
from dataclasses import dataclass

from app_types.bulletin import Bulletin
from app_types.grades import Grade
from app_types.modules import Module


@dataclass
class SmtpConfig:
    email_address: str | None = os.environ.get("EMAIL_ADDRESS", None)
    email_token: str | None = os.environ.get("EMAIL_TOKEN", None)
    smtp_server: str | None = os.environ.get("SMTP_SERVER", None)
    smtp_server_port: int = int(os.environ.get("SMTP_PORT", 0))

    def is_valid(self):
        return all(
            [
                self.email_address,
                self.email_token,
                self.smtp_server,
                self.smtp_server_port,
            ]
        )


SMTP_CONFIG_DATA = SmtpConfig()

TO = os.environ.get(
    "NOTIFIER_EMAIL", os.environ.get("GAPS_USERNAME", "") + "@heig-vd.ch"
)


def __send(smtp_data: SmtpConfig, to: str, subject: str, message_content: str):

    if not smtp_data.is_valid():
        return
    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = smtp_data.email_address
    message["To"] = to
    message.set_content(message_content)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        smtp_data.smtp_server,
        smtp_data.smtp_server_port,
        context=context,
    ) as server:
        server.login(smtp_data.email_address, smtp_data.email_token)
        server.send_message(message)


def get_smtp_auth_data() -> SmtpConfig:
    return SMTP_CONFIG_DATA


def get_destination_email() -> str:
    return TO


def send_email_message(subject: str, message: str) -> None:
    smtp_data = get_smtp_auth_data()
    if not smtp_data.is_valid():
        return
    to = get_destination_email()
    __send(smtp_data, to, subject, message)


def send_bulletin_email(bulletin: Bulletin) -> None:
    smtp_data = get_smtp_auth_data()
    if not smtp_data.is_valid():
        print("smtp data not valid")
        return
    to = get_destination_email()
    subject = "Bulletin"
    message = str(bulletin)
    __send(smtp_data, to, subject, message)
