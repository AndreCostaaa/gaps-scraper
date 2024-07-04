from app_types.bulletin import Bulletin, BulletinGrade, BulletinModule, BulletinUnit
from bs4 import BeautifulSoup


def parse_bulletin(html: str) -> Bulletin:
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", {"id": "record_table"})
    if not table:
        raise ValueError("Can't seem to find a bulletin in this html.")

    rows = table.find_all("tr", recursive=True)

    modules: list[BulletinModule] = []
    for row in rows:
        if len(row["class"]) != 1:
            continue
        cols = row.find_all("td")
        if len(cols) < 7:
            continue

        acronym = cols[0].text
        full_name = cols[1].text
        grade = float(cols[4].text) if cols[4].text != "" else None
        if "module" in row["class"][0]:
            modules.append(
                BulletinModule(
                    units=[],
                    acronym=acronym,
                    name=full_name,
                    status=cols[2].text,
                    grade=grade,
                )
            )
        elif "unit" in row["class"][0]:
            info_list = list(cols[1].stripped_strings)
            if len(info_list) == 0:
                continue
            grades = []
            for i in range(1, len(info_list), 2):
                splitted = info_list[i].split(" ")

                grade_type = splitted[0]  # Cours Laboratoire Projet
                grade_weight = int(
                    splitted[1].replace("(", "").replace(")", "").replace("%", "")
                )  # 20 30 50
                grades.append(
                    BulletinGrade(
                        identifier=grade_type,
                        weight=grade_weight,
                        grade=float(info_list[i + 1]),
                    )
                )

            modules[-1].units.append(
                BulletinUnit(
                    acronym=acronym,
                    name=info_list[0],
                    bulletin_grades=grades,
                    grade=grade,
                )
            )
    return Bulletin(modules)
