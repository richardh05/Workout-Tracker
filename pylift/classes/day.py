from datetime import date, datetime
import json
from pathlib import Path

from pandas import DataFrame

from pylift.classes.exercise_type import ExerciseType
from pylift.classes.workout import Workout
from pylift.utils.dialogues import exercise_type_dialogue


class Day:
    def __init__(self, date: date, workouts: list[Workout]) -> None:
        self.date = date
        self.workouts = workouts

    def __str__(self) -> str:
        return self.date_str

    @property
    def date_str(self) -> str:
        return self.date.strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        return {
            "date": self.date_str,
            "workouts": [w.to_dict() for w in self.workouts],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Day":
        dat = datetime.strptime(data["date"], "%Y-%m-%d").date()
        workouts = [Workout.from_dict(w) for w in data["workouts"]]
        return cls(date=dat, workouts=workouts)

    @classmethod
    def read(cls, filepath: Path) -> "Day":
        with filepath.open() as f:
            data: dict = json.load(f)
        return cls.from_dict(data)

    def to_dataframe(self, types: list[ExerciseType]) -> DataFrame:
        type_map = {et.name: et for et in types}
        data = [
            {
                "date": self.date_str,
                "exercise": workout.exercise_type,
                "category": type_map[workout.exercise_type].category,
                "reps": s.reps,
                "value": s.value,
                "unit": type_map[workout.exercise_type].unit,
                "note": workout.note,
            }
            for workout in self.workouts
            if workout.exercise_type in type_map
            for s in workout.sets
        ]
        return DataFrame(data)

    @staticmethod
    def save(d: "Day", exercises: list[ExerciseType], filepath: Path) -> None:
        def ensure_exercise_type_exists(
            d: Day, exercises: list[ExerciseType],
        ) -> list[ExerciseType]:
            for w in d.workouts:
                if not any(et.name == w.exercise_type for et in exercises):
                    e: ExerciseType = exercise_type_dialogue(w.exercise_type)
                    ExerciseType.save(e, filepath)
                    exercises.append(e)
            return exercises

        def merge_day(old: dict, new: dict) -> dict:
            old_workouts = old["workouts"]
            for new_workout in new["workouts"]:
                # check if this exact workout already exists
                if not any(new_workout == old_workout for old_workout in old_workouts):
                    old_workouts.append(new_workout)
            return old

        def write_day(data: dict[str, str | dict], filename: Path) -> None:
            if filename.exists():
                with filename.open() as f:
                    existing_data = json.load(f)
                merged_data = merge_day(existing_data, data)
            else:
                merged_data = data

            with filename.open("w") as f:
                json.dump(merged_data, f, indent=4)

        filename = filepath / f"{d.date_str}.json"
        data: dict = d.to_dict()
        exercises = ensure_exercise_type_exists(d, exercises)
        write_day(data, filename)

    @staticmethod
    def load_days(start: date, end: date, filepath: Path) -> list["Day"]:
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
    def days_to_dataframe(days: list["Day"], types: list[ExerciseType]) -> DataFrame:
        data = []
        for day in days:
            df = day.to_dataframe(types)
            data.append(df)
        return DataFrame(data).reset_index(drop=True)
