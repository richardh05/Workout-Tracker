from pylift.classes.workout import Workout
from tests.factories.exercise_type_factory import ExerciseTypeFactory
from tests.factories.set_factory import SetFactory


class WorkoutFactory(SetFactory, ExerciseTypeFactory):
  def random_workout(self) -> Workout:
    return Workout(
      exerciseType=f"{self.random_exercise_type().name}",
      sets=[self.random_set() for _ in range(self.r.randint(1, 5))],
      note=f"Note {self.r.randint(1, 10)}"
    )

  def random_workouts(self, count: int|None = None) -> list[Workout]:
    if count is None: 
      count = self.r.randint(1, 6)
    return [self.random_workout() for _ in range(count)]
