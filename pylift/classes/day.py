from datetime import datetime, date
import json
from pathlib import Path
from typing import List
from pandas import DataFrame
from pylift.classes.exercise_type import ExerciseType
from pylift.classes.workout import Workout
from pylift.utils.dialogues import ExerciseTypeDialogue


class Day():
    def __init__(self, date:date, workouts:List[Workout]):
        self.date = date
        self.workouts = workouts

    def __str__(self): return self.date_str

    def __repr__(self):
        return f"Day(date={self.date!r}, workouts={self.workouts!r})"

    def __eq__(self, other):
        if not isinstance(other, Day):
            return NotImplemented
        return self.date == other.date and self.workouts == other.workouts

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
        dat = datetime.strptime(data['date'], "%Y-%m-%d").date()
        workouts = [Workout.from_dict(w) for w in data['workouts']]
        return cls(date=dat, workouts=workouts)
    
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
    
    @staticmethod
    def save(d: 'Day', l:List[ExerciseType], filepath: Path) -> None:
        def ensure_exercise_type_exists(d: Day, l: List[ExerciseType]) -> List[ExerciseType]:
            for w in d.workouts:
                if not any(et.name == w.exerciseType for et in l):
                    e:ExerciseType = ExerciseTypeDialogue(w.exerciseType)
                    ExerciseType.save(e, filepath)
                    l.append(e)
            return l
            
        def merge_day(old: dict, new: dict) -> dict:
            old_workouts = old['workouts']
            for new_workout in new['workouts']:
                # check if this exact workout already exists
                if not any(new_workout == old_workout for old_workout in old_workouts):
                    old_workouts.append(new_workout)
            return old
        
        def write_day(data: dict[str,str|dict], filename: Path) -> None:
            if filename.exists():
                with open(filename, 'r') as f:
                    existing_data = json.load(f)
                merged_data = merge_day(existing_data, data)
            else:
                merged_data = data
                
            filename.parent.mkdir(parents=True, exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(merged_data, f, indent=4)

        
        filename = filepath / f"{d.date_str}.json"
        data: dict = d.to_dict()
        l = ensure_exercise_type_exists(d, l)
        write_day(data, filename)

    @staticmethod
    def load_days(start:date, end:date, filepath:Path) -> List['Day']:
        days = []
        current_date = start
        while current_date <= end:
            filename = filepath / f"{current_date.strftime('%Y-%m-%d')}.json"
            if filename.exists():
                day = Day.read(filename)
                days.append(day)
            current_date = current_date.replace(day=current_date.day + 1)
        return days
    
    @staticmethod
    def days_to_dataframe(days:List['Day'], types:List[ExerciseType]) -> DataFrame:
        data = []
        for day in days:
            df = day.to_dataframe(types)
            data.append(df)
        return DataFrame(data).reset_index(drop=True)