from gaps.gaps import fetch_html
from parser.schedule import parse_schedule
from utils.school_year import get_current_school_year


def fetch_schedule(session_id: str | None) -> dict[str, str]:
    if not session_id:
        return {}

    result: dict[str, str] = {}
    for tri in [1, 3]:
        html = fetch_html(
            f"consultation/horaires/?annee={get_current_school_year()}&trimestre={tri}&type=2",
            session_id,
        )
        result.update(parse_schedule(html))

    return result
