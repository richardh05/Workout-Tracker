import datetime
from pathlib import Path
import unittest
import pandas as pd
from pylift.DataClasses import ExerciseType, Workout, Day, Set

class TestDataClasses(unittest.TestCase):

    def test_saving_Day(self):
        workout = Workout("Ab Crunch", [
                    Set(10, 20.0),
                    Set(12, 22.5)], 
                    "Felt good today")
        workout2 = Workout("Bench Press", [
                    Set(8, 60.0),
                    Set(10, 65.0)], 
                    "Struggled with the last set")

        d = Day ( 
            datetime.date(2023, 10, 1), 
            workouts=[workout, workout2])
        d.save(Path("/home/richard/Documents/"))

        d2 = Day.read(Path("/home/richard/Documents/2023-10-01.json"))
        self.assertEqual(d, d2)

    def test_to_dataframe(self):
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

        d = Day(datetime.date(2023, 10, 1), workouts=[workout, workout2])
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


if __name__ == '__main__':
    unittest.main()
