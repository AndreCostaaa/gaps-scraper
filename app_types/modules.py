from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Module:
    name: str
    average: str
