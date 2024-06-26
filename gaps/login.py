import requests

from gaps.gaps import url
from gaps.student import get_student_id


def login(username, password) -> tuple [str | None, str]:
    data = {"login": username, "password": password, "submit": "Entrer"}

    req = requests.post(
        url("consultation/index.php"),
        data=data,
        headers={
            "User-Agent": "Mozilla/5.0 (Linux x86_64)",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    session_id = req.cookies.get_dict().get("GAPSSESSID")
    student_id = get_student_id(session_id)
    return session_id, student_id
