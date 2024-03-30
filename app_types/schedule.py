from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class ModuleClass:
    module: str
    class_identifier: str
