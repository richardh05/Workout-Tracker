from dataclasses import dataclass
from pandas import DataFrame

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
    
    @classmethod
    def from_dataframe(cls, df:DataFrame) -> "Workout":
        et = df["Excersise"].iloc[0]

        # collapse notes into one string (skip NaN/None)
        note_series = df["Notes"].dropna().astype(str)
        note = "; ".join(note_series) if not note_series.empty else None
        
        # build Set objects row by row
        sets = []
        for _, row in df.iterrows():
            sets.append(
                Set(
                    value=row["Value"],
                    reps=row["Reps"]
                )
            )

        return cls(exercise_type=et, sets=sets, note=note)
        
        
