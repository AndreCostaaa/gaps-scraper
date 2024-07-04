from app_types.bulletin import Bulletin
from gaps.gaps import fetch_html
from parser.bulletin import parse_bulletin
from utils.school_year import get_current_school_year


def fetch_current_bulletin(session_id: str, student_id: str) -> Bulletin:

    html = fetch_html(
        f"consultation/notes/bulletin.php?id={student_id}",
        session_id,
    )
    return parse_bulletin(html)


def fetch_provisional_bulletin(session_id: str, student_id: str) -> Bulletin | None:
    for i in range(0, 10):
        html = fetch_html(
            f"consultation/etudiant/?doc={student_id}_{i:02d}_{get_current_school_year()}_p_grades_fr.pdf",
            session_id,
        )
        if (
            "Vous n'avez pas les droits nécessaires pour télécharger ce document."
            in html
        ):
            continue
        return parse_bulletin(html)

    for i in range(0, 100):
        html = fetch_html(
            f"consultation/etudiant/?doc={student_id}_{i}_{get_current_school_year()}_p_grades_fr.pdf",
            session_id,
        )
        if (
            "Vous n'avez pas les droits nécessaires pour télécharger ce document."
            in html
        ):
            continue
        return parse_bulletin(html)

    return None
