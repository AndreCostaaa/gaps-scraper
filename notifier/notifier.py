from notifier.email import send_email_notification
from notifier.gaps_notifier import GapsNotifierHandler
from app_types.grades import Grade

from app_types.modules import Module

gaps_notifier = GapsNotifierHandler()


def notify(grades: list[Grade], modules: list[Module]):
    if not grades:
        return
    send_email_notification(grades, modules)
    for grade in grades:
        gaps_notifier.send_grade(grade)
