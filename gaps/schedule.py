from gaps.gaps import fetch_html
from parser.schedule import parse_schedule, ModuleClass


def fetch_schedule(session_id: str| None) -> dict[str, str]:
    if not session_id:
        return {}
    html = fetch_html("consultation/horaires/", session_id)

    return parse_schedule(html)
