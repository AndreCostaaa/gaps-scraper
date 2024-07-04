from gaps.bulletin import fetch_provisional_bulletin
from gaps.login import login
from notifier.email import send_bulletin_email
from utils.file_io import get_last_prov_bulletin_save, save_prov_bulletin

import os
from datetime import datetime


def should_run():
    FRIDAY = 4
    FEB = 2
    JULY = 7
    DAYS_IN_A_MONTH = 31
    now = datetime.now()
    curr_month = now.month
    curr_weekday = now.weekday

    is_prov_bulletin_month = curr_month == FEB or curr_month == JULY
    is_prov_bulletin_weekday = curr_weekday == FRIDAY
    last_bulletin = datetime.fromtimestamp(get_last_prov_bulletin_save())
    last_bulletin_delta = now - last_bulletin
    last_bulletin_delta_bigger_than_one_month = (
        last_bulletin_delta.days > DAYS_IN_A_MONTH
    )

    return (
        is_prov_bulletin_month
        and is_prov_bulletin_weekday
        and last_bulletin_delta_bigger_than_one_month
    )


def main():
    username = os.environ.get("GAPS_USERNAME")
    password = os.environ.get("GAPS_PASSWORD")
    if not should_run():
        print("Not time to run this script")
        return

    session_id, student_id = login(username, password)
    if not session_id:
        print("Failed to login")
        return

    bulletin = fetch_provisional_bulletin(session_id, student_id)
    if not bulletin:
        print("Bulletin not found")
        return

    send_bulletin_email(bulletin)
    save_prov_bulletin(bulletin)


if __name__ == "__main__":
    main()
