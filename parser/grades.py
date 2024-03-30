from dataclasses import dataclass
from bs4 import BeautifulSoup
from app_types.grades import Grade
from app_types.modules import Module


def parse_grades(html) -> list:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "displayArray"})
    if not table:
        return []

    rows = table.find_all("tr")
    grades = []
    modules = []
    curr_module = ""
    for row in rows:
        is_header = "bigheader" in str(row)
        is_grade = "bodyCC" in str(row)

        if is_grade:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue
            grade_name = cols[1].text
            class_average = cols[2].text
            grade = cols[4].text
            if grade == "-":
                continue
            grades.append(Grade(curr_module, grade, grade_name, class_average))
        elif is_header:
            line_split = row.text.split(" ")
            curr_module = line_split[0]
            modules.append(Module(curr_module, line_split[-1]))

    return grades, modules
