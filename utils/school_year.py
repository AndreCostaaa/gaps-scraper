from datetime import datetime


def get_current_school_year() -> int:

    now = datetime.now()
    year = now.year

    if now.month < 8:
        year -= 1

    return year


def get_current_trimester() -> int:

    now = datetime.now()
    if now.month == 8 or (now.month == 9 and now.day < 20):
        return 0
    if now.month > 9 or now.month < 2:
        return 1
    return 3


def get_next_trimester() -> int:
    now = datetime.now()
    if now.month == 8 or (now.month == 9 and now.day < 20):
        return 1
    if now.month > 9 or now.month < 2:
        return 3
    return 0


def trimester_name(trimester: int) -> str:
    if trimester == 0:
        return "Summer"
    if trimester == 1:
        return "S1"
    if trimester == 3:
        return "S2"
    return f"Unknown trimester ({trimester})"
