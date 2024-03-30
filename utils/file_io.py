import json
import os

from app_types.grades import Grade


GRADES_FILE_PATH = "/app/data/grades.json"


def read_json_file(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return json.load(f)


def write_json_file(file_path: str, data: dict | list):
    with open(file_path, "w+") as f:
        json.dump(data, f)


def save_grades(grades: list[Grade]):

    write_json_file(GRADES_FILE_PATH, [grade.to_dict() for grade in grades])


def read_grades() -> list:
    try:
        return [Grade.from_dict(grade) for grade in read_json_file(GRADES_FILE_PATH)]
    except Exception:
        return []
