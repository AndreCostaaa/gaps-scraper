from datetime import datetime


def get_current_school_year() -> int:

    now = datetime.now()
    year = now.year

    if now.month < 8:
        year -= 1

    return year
