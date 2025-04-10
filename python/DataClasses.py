from typing import List, Optional
import pandas

class Workout:
    def __init__(self, exerciseType:str, sets:pandas.DataFrame, note:Optional[str] = None):
        self.exercise_type = exerciseType
        self.sets = sets
        self.note = note

class Day:
    def __init__(self, date:str, workouts:Optional[List[Workout]] ):
        self.date = date
        self.workouts = workouts
    def __str__(self):
        return self.date
