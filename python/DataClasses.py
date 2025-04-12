from typing import List, Optional
from dataclasses import dataclass
import pandas as pd

@dataclass
class ExerciseType:
    name:str
    unit:str
    category:str

@dataclass
class Workout:
    exerciseType:int
    sets:pd.DataFrame
    note:Optional[str]
    def __str__(self):
        return self.exerciseType

@dataclass
class Day:
    date:str
    workouts:Optional[List[Workout]]
    def __str__(self):
        return self.date
