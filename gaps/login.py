import requests

from gaps.gaps import url
from gaps.student import get_student_id


def login(username, password) -> str | None:
    data = {"login": username, "password": password, "submit": "Entrer"}

    req = requests.post(
        url("consultation"),
        data=data,
        headers={
            "User-Agent": "Mozilla/5.0 (Linux x86_64)",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    if "Connexion échouée" in req.text:
        return None, None

    session_id = req.cookies.get_dict().get("GAPSSESSID")
    student_id = get_student_id(session_id)
    return session_id, student_id
