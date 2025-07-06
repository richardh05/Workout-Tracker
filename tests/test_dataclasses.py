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

        day = Day ( 
            datetime.date(2023, 10, 1), 
            workouts=[workout, workout2])
        day.save(Path("/home/richard/Documents/"))

        day2 = Day.read(Path("/home/richard/Documents/2023-10-01.json"))
        self.assertEqual(day, day2)


if __name__ == '__main__':
    unittest.main()
