from dataclasses import dataclass
from enum import Enum


class UnitCategory(Enum):
    DISTANCE = 1
    WEIGHT = 2
    TIME = 3
    VOLUME = 4
    SPEED = 5


@dataclass
class Unit:
    """
    Represents a unit of measurement for a lift, such as "kg" or "lbs".
    """

    long_name: str
    short_name: str
    category: UnitCategory

    def __str__(self) -> str:
        return self.short_name

    def __repr__(self) -> str:
        return f"Unit(name={self.short_name!r})"

    def to_dict(self) -> dict:
        return {
            "long_name": self.long_name,
            "short_name": self.short_name,
            "category": self.category.name,
        }
