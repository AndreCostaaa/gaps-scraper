from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class BulletinGrade:
    identifier: str
    grade: float
    weight: int

    def __repr__(self) -> str:
        return f"{self.identifier} ({self.weight}%) - {self.grade}"


@dataclass(eq=True, frozen=True)
class BulletinUnit:
    acronym: str
    name: str
    bulletin_grades: list[BulletinGrade]
    grade: float | None

    def __repr__(self) -> str:
        repr = f"({self.acronym}) {self.name} - {self.grade}"
        for grade in self.bulletin_grades:
            repr += f"\n\t\t{grade}"
        return repr


@dataclass()
class BulletinModule:
    units: list[BulletinUnit]
    grade: float | None
    status: str
    acronym: str
    name: str

    def __repr__(self) -> str:
        repr = f"({self.acronym}) {self.name} - {self.status} - {self.grade}"

        for unit in self.units:
            repr += f"\n\t{unit}"

        return repr


@dataclass(eq=True, frozen=True)
class Bulletin:
    modules: list[BulletinModule]

    def __repr__(self) -> str:
        repr = ""
        for module in self.modules:
            repr += f"\n{module}"
        return repr
