from typing import List, Optional
import pandas

class ExerciseType:
    def _init__(self, name:str, unit:str, category:str):
        self.name = name
        self.unit = unit
        self.category = category

class Workout:
    def __init__(self, exerciseType:str, sets:pandas.DataFrame, note:Optional[str] = None):
        self.exercise_type = exerciseType
        self.sets = sets
        self.note = note
    def __str__(self):
        return self.exercise_type

class Day:
    def __init__(self, date:str, workouts:Optional[List[Workout]] ):
        self.date = date
        self.workouts = workouts
    def __str__(self):
        return self.date
