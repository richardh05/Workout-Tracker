from typing import List, Optional
from dataclasses import dataclass
import pandas as pd

@dataclass
class ExerciseType:
    id:Optional[int]
    name:str
    unit:str
    category:str

@dataclass
class Workout:
    id:Optional[int]
    exerciseType:ExerciseType
    sets:pd.DataFrame
    note:Optional[str]
    def __str__(self):
        return self.note

@dataclass
class Day:
    id:Optional[int]
    date:str
    workouts:List[Workout]
    def __str__(self):
        return self.date
