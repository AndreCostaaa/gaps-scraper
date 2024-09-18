from gaps.gaps import fetch_html
from parser.grades import parse_grades
from app_types.grades import Grade
from app_types.modules import Module
import json


def __fetch_html(session_id, student_id, year) -> str:
    html = fetch_html(
        f"consultation/controlescontinus/consultation.php?idst={student_id}&year={year}",
        session_id,
        data={
            "rs": "replaceHtmlPart",
            "rsargs": '["result",null]',
        },
        is_post=True,
    )

    html = html.replace("+:", "")
    obj = json.loads(json.loads(html))

    return obj["parts"]["result"]


def fetch_grades(session_id, student_id, year) -> tuple[list[Grade], list[Module]]:
    html = __fetch_html(session_id, student_id, year)

    return parse_grades(html)
