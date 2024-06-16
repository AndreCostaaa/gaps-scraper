from bs4 import BeautifulSoup


def parse_schedule(html: str) -> dict[str, str]:  # eg {"PDL":"A", "MATH":"B"}

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
