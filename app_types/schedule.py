from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class ModuleClass:
    module: str
    class_identifier: str

@dataclass(eq=True, frozen=True)
class ScheduleClass:
    module: str
    class_identifier: str
    course_identifier: str
    teachers: list[str]
    room: str
    day_index: int
    start_time_index: int
    start_time: str
    duration: int

class Schedule:
    def __init__(self):
        self.classes: list[ScheduleClass] = []
        self.max_rows = 0
        self.max_cols = 0

    def add_class(self, c: ScheduleClass):
        if c.start_time_index + 1 > self.max_cols:
            self.max_cols = c.start_time_index + 1
        if c.day_index + 1 > self.max_rows:
            self.max_rows = c.day_index + 1
        self.classes.append(c)

