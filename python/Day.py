from typing import List, Optional
import Workout

class Day:
    def __init__(self, date:str, workouts:Optional[List[Workout.Workout]] ):
        self.date = date
        self.workouts = workouts
        