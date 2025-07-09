from typing import List, Optional
from dataclasses import dataclass
from pylift.classes.set import Set

@dataclass
class Workout:
    exerciseType:str
    sets:List[Set]
    note:Optional[str]

    def to_dict(self) -> dict:
        return {
        "exerciseType": self.exerciseType,
        "sets": [s.to_dict() for s in self.sets],
        "note": self.note
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Workout':
        sets = [Set.from_dict(s) for s in data['sets']]
        return cls(
            exerciseType=data['exerciseType'],
            sets=sets,
            note=data.get('note', None)
        )