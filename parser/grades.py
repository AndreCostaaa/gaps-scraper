from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class Grade:
    course: str
    grade: str
    name: str


def parse_headers(html) -> list:
    soup = BeautifulSoup(html, "html.parser")
    headers = soup.find(attrs={"class": "bigheader"})
    headers = []
    for header in headers:
        headers.add(header.text)

    return headers


def parse_grades(html) -> list:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "displayArray"})
    lines = table.text.split("\n")
    module_headers = set(parse_headers(html))
    results = {}
    averages = {}
    module = ""
    for i, line in enumerate(lines):
        is_header = line in module_headers
        is_grade = "%" in line

        if is_grade:
            grade_name = lines[i - 1]
            splitted = line.split(" ")
            try:
                float(splitted[-1])
                results[module + " " + grade_name] = f"{splitted[-1]} ({splitted[0]})"
            except ValueError:
                pass

        if is_header:
            line_split = line.split(" ")
            module = line_split[0]
            averages[module] = line_split[-1]

    return results, averages
