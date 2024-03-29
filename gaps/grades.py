from gaps.gaps import fetch_html
from parser.grades import parse_grades


def __fetch_html(session_id, student_id, year) -> str:
    html = fetch_html(
        f"consultation/controlescontinus/consultation.php",
        session_id,
        params={"idst": student_id, "year": year},
    )

    return html


def fetch_grades(session_id, student_id, year) -> list:
    html = __fetch_html(session_id, student_id, year)

    grades = parse_grades(html)
    print(grades)
