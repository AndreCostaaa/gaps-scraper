from app_types.grades import Grade
from gaps.grades import fetch_grades
from gaps.login import login
from gaps.schedule import fetch_schedule
import os
from notifier.notifier import notify_grades
from utils.school_year import get_current_school_year
from utils.file_io import read_grades, save_grades


def main():
    username = os.environ.get("GAPS_USERNAME")
    password = os.environ.get("GAPS_PASSWORD")

    session_id, student_id = login(username, password)
    if not student_id:
        print("Failed to login")
        return

    grades, modules = fetch_grades(session_id, student_id, get_current_school_year())

    old_grades = read_grades()

    if grades == old_grades:
        print("No new grades")
        return

    class_identifiers = fetch_schedule(session_id)

    new_grades: list[Grade] = [
        Grade(
            grade.course,
            grade.grade,
            grade.name,
            grade.class_average,
            class_identifiers.get(grade.course, grade.course),
        )
        for grade in grades
        if grade not in old_grades
    ]

    notify_grades(new_grades, modules)
    save_grades(grades)


if __name__ == "__main__":
    main()
