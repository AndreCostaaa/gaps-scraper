from gaps.grades import fetch_grades
from gaps.login import login
from getpass import getpass


def main():
    session_id, student_id = login(input("Username: "), getpass("Password: "))
    if not student_id:
        print("Login failed")
        return

    fetch_grades(session_id, student_id, "2023")


if __name__ == "__main__":
    main()
