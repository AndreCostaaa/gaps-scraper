from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Grade:
    course: str
    grade: str
    name: str
    class_average: str
    class_identifier: str = "X"

    def from_dict(data):
        return Grade(data["course"], data["grade"], data["name"], data["class_average"])

    def to_dict(self):
        return {
            "course": self.course,
            "grade": self.grade,
            "name": self.name,
            "class_average": self.class_average,
            "class": self.class_identifier,
        }
