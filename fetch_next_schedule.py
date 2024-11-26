from gaps.login import login
from gaps.schedule import is_schedule_available
import os
from notifier.notifier import notify_new_schedule
from utils.school_year import (
    get_current_school_year,
    get_next_trimester,
)
from utils.file_io import get_schedule_data_path

import pathlib


def main():
    username = os.environ.get("GAPS_USERNAME")
    password = os.environ.get("GAPS_PASSWORD")

    session_id, _ = login(username, password)
    if not session_id:
        print("Failed to login")
        return

    next_trimester = get_next_trimester()
    year = get_current_school_year()
    if next_trimester == 0:
        year += 1

    print(f"Fecthing Schedule for {year}-{next_trimester}")

    year = get_current_school_year()
    if next_trimester == 0:
        year += 1

    if not is_schedule_available(session_id, year, next_trimester):
        print("New Schedule is not available")
        return

    schedule_path = get_schedule_data_path(year, next_trimester)
    if os.path.exists(schedule_path):
        print("New Schedule already transmitted")
        return

    notify_new_schedule(year, next_trimester)
    pathlib.Path(schedule_path).touch(exist_ok=True)


if __name__ == "__main__":
    main()
