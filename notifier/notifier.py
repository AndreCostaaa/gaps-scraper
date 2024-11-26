from notifier.email import send_email_message
from notifier.gaps_notifier import GapsNotifierHandler
from app_types.grades import Grade

from app_types.modules import Module
from utils.school_year import trimester_name

gaps_notifier = GapsNotifierHandler()


def notify_grades(grades: list[Grade], modules: list[Module]):
    if not grades:
        return
    email_subject = build_grades_email_subject(grades)
    email_message = build_grades_email_message(grades, modules)
    print(email_message)
    send_email_message(email_subject, email_message)
    for grade in grades:
        gaps_notifier.send_grade(grade)


def build_grades_email_subject(grades: list[Grade]) -> str:
    return "New grade" + ("s" if len(grades) > 1 else "")


def build_grades_email_message(grades: list[Grade], modules: list[Module]) -> str:
    message = "New grades: \n"
    for grade in grades:
        message += (
            f"{grade.course} - {grade.name} - {grade.grade} ({grade.class_average})\n"
        )

    message += "\n\nModules:\n"
    for module in modules:
        message += f"{module.name} - {module.average}\n"

    return message


def notify_new_schedule(school_year: int, trimester: int):

    email_subject = "New Schedule Available"
    email_message = (
        f"Schedule for {school_year} - {trimester_name(trimester)} is now available\n"
    )
    send_email_message(email_subject, email_message)
