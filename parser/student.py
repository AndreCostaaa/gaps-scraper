def parse_student_id(html: str) -> str:
    STUDENT_ID_CONST_NAME = "const DEFAULT_STUDENT_ID"
    STUDENT_ID_START_TOKEN = "= "
    STUDENT_ID_END_TOKEN = ";"

    identifier = html.find(STUDENT_ID_CONST_NAME)
    start = html.find(STUDENT_ID_START_TOKEN, identifier)
    end = html.find(STUDENT_ID_END_TOKEN, start)
    if identifier == -1 or start == -1 or end == -1:
        raise ValueError(f"Could not find student id")
    return html[start + len(STUDENT_ID_START_TOKEN) : end]
