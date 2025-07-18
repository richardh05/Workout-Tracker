from dataclasses import dataclass

from pylift.classes.set import Set


@dataclass
class Workout:
    exercise_type: str
    sets: list[Set]
    note: str | None

    def to_dict(self) -> dict:
        return {
            "exerciseType": self.exercise_type,
            "sets": [s.to_dict() for s in self.sets],
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Workout":
        sets = [Set.from_dict(s) for s in data["sets"]]
        return cls(
            exercise_type=data["exerciseType"],
            sets=sets,
            note=data.get("note"),
        )
