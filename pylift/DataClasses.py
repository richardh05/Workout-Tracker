from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path
from pandas import DataFrame
import json
import datetime

# Data Classes for Workout Tracker


class Savable(ABC):
    """
    Base class for objects that can be saved as JSON.
    """

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    def write(self, filepath: Path) -> None:
        data: dict = self.to_dict()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    @abstractmethod
    def read(cls, filepath: Path) -> 'Savable':
        """
        Load an instance from JSON file.
        """
        pass
        
    

# Exercise types used in workouts, such as "Bench Press", "Squat", etc.


@dataclass
class ExerciseType:
    name:str
    unit:str
    category:str

    @property
    def json(self) -> dict:
        return {
            "name": self.name,
            "unit": self.unit,
            "category": self.category
        }
    
class ExerciseTypes(Savable):
    def __init__(self, exerciseTypes: List['ExerciseType']):
        self.exerciseTypes = exerciseTypes
    
    def to_dict(self) -> dict:
        return {"ExerciseTypes": [et.json for et in self.exerciseTypes]}
    
    def save(self, filepath: Path) -> None:
        self.write(filepath / "ExerciseTypes.json")

# The actual records of workouts
@dataclass
class Set:
    reps:int
    value:float

    def to_dict (self) -> dict:
        return {
            "reps": self.reps,
            "value": self.value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Set':
        return cls(
        reps=data['reps'],
        value=data['value']
        )
    

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

@dataclass
class Day(Savable):
    date:datetime.date
    workouts:List[Workout]
    def __str__(self): return self.date_str

    @property
    def date_str(self) -> str:
        return self.date.strftime("%Y-%m-%d")
    
    def to_dict(self) -> dict:
        return {
            "date": self.date_str,
            "workouts": [w.to_dict() for w in self.workouts]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Day':
        date = datetime.datetime.strptime(data['date'], "%Y-%m-%d").date()
        workouts = [Workout.from_dict(w) for w in data['workouts']]
        return cls(date=date, workouts=workouts)
    
    def save(self, filepath: Path) -> None:
        filename = filepath / f"{self.date_str}.json"
        self.write(filename)

    @classmethod
    def read(cls, filepath: Path) -> 'Day':
        with open(filepath, 'r') as f:
            data:dict = json.load(f)
        return cls.from_dict(data)
    
    def to_dataframe(self, types:List[ExerciseType]) -> DataFrame:
        data = []
        for workout in self.workouts:
            ex = next((et for et in types if et.name == "Squat"))
            for s in workout.sets:
                data.append({
                    "date": self.date_str,
                    "exercise": workout.exerciseType,
                    "category": ex.category,
                    "reps": s.reps,
                    "value": s.value,
                    "unit": ex.unit,
                    "note": workout.note
                })
        return DataFrame(data)
