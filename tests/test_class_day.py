from datetime import date
from pathlib import Path
from typing import List
import pytest
import pandas as pd
from pylift.classes.day import ExerciseType, Workout, Day
from pylift.classes.set import Set
from tests.factories.day_factory import DayFactory

seeds = [42, 123, 456]

@pytest.fixture(params=seeds)
def rng(request) -> DayFactory:
    return DayFactory(seed=request.param)

@pytest.fixture
def sample_date():
    return date(2023, 10, 1)

@pytest.mark.parametrize("note", ["Felt Strong","Not Bad"])
def test_init(rng, note):
    date = rng.random_date()
    my_workouts = rng.random_workouts
    day = Day(date, my_workouts)
    assert day.date == date
    assert day.workouts == my_workouts

def test_str(rng):
    d = rng.random_date_str()
    day = Day(d.get("date"), [])
    assert str(day) == d.get("str")

def test_repr(rng):
    date = rng.random_date()
    my_workouts = rng.random_workouts
    day = Day(date, my_workouts)
    expected_repr = f"Day(date={date!r}, workouts={day.workouts!r})"
    assert repr(day) == expected_repr

@pytest.mark.parametrize(
    "same_date, same_workouts, expected_equal",
    [
        (True, True, True),       # 1. same date and same workouts → equal
        (False, True, False),     # 2. different date → not equal
        (True, False, False),     # 3. same date, different workouts → not equal
    ]
)
def test_eq(rng, sample_date, same_date, same_workouts, expected_equal):
    # build day1
    workouts1 = [Workout("Squat", [Set(10, 50.0)], "Note")]
    day1 = Day(sample_date, workouts1)

    # build day2 based on flags
    date2 = sample_date if same_date else rng.random_date()
    workouts2 = workouts1 if same_workouts else []  # or rng.random_workouts() for more variety
    day2 = Day(date2, workouts2)

    assert (day1 == day2) is expected_equal

def test_to_dict():
    dat = date(2023, 10, 1)
    workout = Workout("Squat", [Set(10, 50.0)], "Felt strong")
    day = Day(dat, [workout])
    expected_dict = {
        "date": "2023-10-01",
        "workouts": [workout.to_dict()]
    }
    assert day.to_dict() == expected_dict

def test_save(rng, tmp_path:Path):
    d = rng.random_day()
    test_file = tmp_path / f"{d.date_str}.json"
    l = rng.exercise_types()

    d.save(d, l, tmp_path)
    d2 = Day.read(test_file)
    assert d == d2

def test_to_dataframe(rng):
    et = rng.exercise_types()

    workout = Workout("Squat", [
        Set(10, 50.0),
        Set(12, 55.0)], 
        "Good form")
    workout2 = Workout("Deadlift", [
        Set(8, 70.0),
        Set(10, 75.0)], 
        "Felt strong")
    types = [
        ExerciseType("Squat", "Kg", "Lower Body"),
        ExerciseType("Deadlift", "Kg", "Lower Body")
    ]

    d = Day(date(2023, 10, 1), workouts=[workout, workout2])
    df = d.to_dataframe(types)

    expected_data = {
        "date": ["2023-10-01", "2023-10-01", "2023-10-01", "2023-10-01"],
        "exercise": ["Squat", "Squat", "Deadlift", "Deadlift"],
        "category": ["Lower Body", "Lower Body", "Lower Body", "Lower Body"],
        "reps": [10, 12, 8, 10],
        "value": [50.0, 55.0, 70.0, 75.0],
        "unit": ["Kg", "Kg", "Kg", "Kg"],
        "note": ["Good form", "Good form", "Felt strong", "Felt strong"]
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(df, expected_df)
