import requests
from gaps.gaps import fetch_html, url
from parser.student import parse_student_id


def get_student_id(session_id) -> str:
    html = fetch_html("consultation/etudiant/", session_id)

    student_id = parse_student_id(html)
    return student_id
