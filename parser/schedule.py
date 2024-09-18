from bs4 import BeautifulSoup

from app_types.schedule import Schedule, ScheduleClass


def parse_classes_from_schedule(html: str) -> dict[str, str]:  # eg {"PDL":"A", "MATH":"B"}

    soup = BeautifulSoup(html, "html.parser")
    teaching_cols = soup.findAll("a", {"class": "teaching"})
    if not teaching_cols:
        return {}

    modules = {}
    for col in teaching_cols:
        splitted = col.text.split("-")

        class_identifier = splitted[-2]
        module = "-".join(splitted[0:-2])
        modules[module] = class_identifier

    return modules

def parse_schedule(html:str) -> Schedule:

    schedule = Schedule()
    soup = BeautifulSoup(html, "html.parser")
    schedule_table = soup.find("table", {"class": "horaire"})
    if not schedule_table:
        return schedule
    rows = schedule_table.findAll("tr")

    start_time_idx = 0
    for i, row in enumerate(rows[2:]):
        cols = row.findAll("td")
        if len(cols) < 1:
            break
        current_start_time = cols[0].text[0:5]
        current_col = 0
        for col in cols[1:]:
            col_span = int(col["colspan"])
            current_col += col_span
            start_time_idx += 1
            if not col.has_attr('class'):
                continue
            if col["class"][0] == "empty":
                continue
            children = col.findChildren("a", recursive=True)
            teaching_a = col.findChild("a", {"class":"teaching"})
            teachers_a = col.findChildren("a", {"class":"teacherAcronym"})
            title_split = teaching_a.text.split("-")
            teachers = []
            for t_a in teachers_a:
                teachers.append(t_a.text)

            room = children[-1].text
            schedule.add_class(ScheduleClass(module=title_split[0],
                                             class_identifier=title_split[1],
                                             course_identifier=title_split[2],
                                             teachers=teachers,
                                             room= room,
                                             start_time=current_start_time,
                                             day_index=(current_col - col_span) // 2,
                                             start_time_index= i - 2,
                                             duration=col["rowspan"]))
    return schedule

