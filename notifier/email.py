from ast import Module
from email.message import EmailMessage
import os
import smtplib
import ssl
from dataclasses import dataclass

from app_types.grades import Grade


@dataclass
class SmtpConfig:
    email_address: str = os.environ.get("EMAIL_ADDRESS")
    email_token: str = os.environ.get("EMAIL_TOKEN")
    smtp_server: str = os.environ.get("SMTP_SERVER")
    smtp_server_port: int = os.environ.get("SMTP_SERVER_PORT")


SMTP_CONFIG_DATA = SmtpConfig()

TO = os.environ.get("NOTIFIER_EMAIL", os.environ.get("GAPS_USERNAME") + "@heig-vd.ch")


def __send(smtp_data: SmtpConfig, to: str, subject: str, message_content: str):

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


def build_email_message(grades: list[Grade], modules: list[Module]) -> str:

    message = "New grades: \n"
    for grade in grades:
        message += (
            f"{grade.course} - {grade.name} - {grade.grade} ({grade.class_average})\n"
        )

    message += "\n\nModules:\n"
    for module in modules:
        message += f"{module.name} - {module.average}\n"

    return message


def get_smtp_auth_data() -> SmtpConfig:
    return SMTP_CONFIG_DATA


def build_subject(grades: list[Grade]) -> str:
    return "New grade" + ("s" if len(grades) > 1 else "")


def get_destination_email() -> str:
    return TO


def send_email_notification(grades: list[Grade], modules: list[Module]) -> None:
    smtp_data = get_smtp_auth_data()
    to = get_destination_email()
    subject = build_subject(grades)
    message = build_email_message(grades, modules)
    print(message)
    __send(smtp_data, to, subject, message)
