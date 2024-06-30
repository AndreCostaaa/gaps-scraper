from parser.schedule import parse_classes_from_schedule, parse_schedule

from app_types.schedule import Schedule
from gaps.gaps import fetch_html
from utils.school_year import get_current_school_year


def fetch_current_schedule(session_id: str) -> Schedule:
    
    html = fetch_html(
            f"consultation/horaires/?annee={get_current_school_year()}&trimestre={3}&type=2",
            session_id,
    )
    return parse_schedule(html)



def fetch_classes(session_id: str | None) -> dict[str, str]:
    if not session_id:
        return {}

    result: dict[str, str] = {}
    for tri in [1, 3]:
        html = fetch_html(
            f"consultation/horaires/?annee={get_current_school_year()}&trimestre={tri}&type=2",
            session_id,
        )
        result.update(parse_classes_from_schedule(html))

    return result
