from datetime import date
import textwrap
from pylift.classes.day import Day
from pylift.classes.set import Set
from pylift.classes.workout import Workout
from tests.factories.workout_factory import WorkoutFactory

class DayFactory(WorkoutFactory):
  def random_day(self) -> Day:
    return Day(
      date=self.random_date(),
      workouts=self.random_workouts()
  )

  def random_days(self, count: int|None = None) -> list[Day]:
    if count is None: 
      count = self.r.randint(1, 6)
    return [self.random_day() for _ in range(count)]

  def random_markdown(self) -> tuple[str, list[Day]]:
    def random_workout_md(workout: Workout) -> str:
      md = f"## {workout.exerciseType}\n{workout.note}\n\n| Value | Reps |\n| ----- | ---- |\n"
      sets_md = "\n".join(f"| {s.value} | {s.reps} |" for s in workout.sets)
      return f"{md}{sets_md}"
    
    def day_md(day: Day) -> str:
      date_str = day.date.strftime("%Y-%m-%d")
      workouts_md = "\n".join(random_workout_md(w) for w in day.workouts)
      return f"# {date_str}\n{workouts_md}"
    
    myDays = self.random_days()
    print ("\n".join(day_md(day) for day in myDays))
    return "\n".join(day_md(day) for day in myDays), myDays

  def static_days(self) -> list[Day]:
    return [
      Day(date=date(2025,4,17), workouts=[
          Workout("Overhead Press", [Set(8,25),Set(8,31.5),Set(8,31.5)], note=""),
          Workout("Bench Press", [Set(8,22),Set(8,22),Set(8,24.5)], note="")
      ]),
      Day(date=date(2025,4,25), workouts=[
          Workout("Deadlift", [Set(10,12),Set(10,12)], note="")
      ]),
      Day(date=date(2025,5,18), workouts=[
          Workout("Lateral Pulldown", [Set(12,25),Set(7,31.5),Set(8,31.5),Set(8,31.5)], note="")
      ]),
      Day(date=date(2025,6,27), workouts=[
          Workout("Bench press", [Set(8,17),Set(8,17),Set(8,22),Set(8,22)], note="")
      ]),
    ]

  def static_markdown(self) -> str:
    return textwrap.dedent("""
      # 2025-04-17
      ## Overhead Press
       
      | Value | Reps |
      | ----- | ---- |
      | 25    | 8    |
      | 31.5  | 8    |
      | 31.5  | 8    |
      ## Bench Press
      
      | Value | Reps |
      | ----- | ---- |
      | 22    | 8    |
      | 22    | 8    |
      | 24.5  | 8    |
      # 2025-04-25
      ## Deadlift
                           
      | Value | Reps |
      | ----- | ---- |
      | 12    | 10   |
      | 12    | 10   |
      # 2025-05-18
      ## Lateral Pulldown
                           
      | Value | Reps |
      | ----- | ---- |
      | 25    | 12   |
      | 31.5  | 7    |
      | 31.5  | 8    |
      | 31.5  | 8    |
      # 2025-06-27
      ## Bench press
                           
      | Reps | Value |
      | ---- | ----- |
      | 8    | 17    |
      | 8    | 17    |
      | 8    | 22    |
      | 8    | 22    |
      """)
  
f = DayFactory(42)
r = f.random_markdown()
print(r[0])