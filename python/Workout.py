from typing import List, Optional
import pandas

class Workout:
    def __init__(self, exerciseType:str, sets:pandas.DataFrame, note:Optional[str] = None):
        self.exercise_type = exerciseType
        self.sets = sets
        self.note = note