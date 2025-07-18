from dataclasses import dataclass


@dataclass
class Set:
    reps: int
    value: float

    def to_dict(self) -> dict:
        return {
            "reps": self.reps,
            "value": self.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Set":
        return cls(
            reps=data["reps"],
            value=data["value"],
        )
