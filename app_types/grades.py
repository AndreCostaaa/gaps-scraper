from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Grade:
    course: str
    grade: str
    name: str
    class_average: str
    class_identifier: str = "X"

    @staticmethod
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

    def __eq__(self, other: object, /) -> bool:
        if type(other) != Grade:
            return False

        return (
            other.course == self.course
            and other.grade == self.grade
            and other.name == self.name
            and other.class_average == self.class_average
            and (
                other.class_identifier == self.class_identifier
                or other.class_identifier == "X"
                or self.class_identifier == "X"
            )
        )
