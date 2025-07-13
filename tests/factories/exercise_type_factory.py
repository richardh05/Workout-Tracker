from pylift.classes.exercise_type import ExerciseType
from tests.factories.factory import Factory


class ExerciseTypeFactory(Factory):
  def exercise_types(self) -> list[ExerciseType]:
    return [
      ExerciseType("Deadlift", "Kg", "Lower Body"),
      ExerciseType("Squat", "Kg", "Legs"),
      ExerciseType("Bench Press", "Kg", "Chest"),
      ExerciseType("Overhead Press", "Kg", "Shoulders"),
      ExerciseType("Ab Crunch", "Reps", "Core")
    ]
  
  def random_exercise_type(self) -> ExerciseType:
    exercise_types = self.exercise_types()
    return exercise_types[self.r.randint(0, len(exercise_types) - 1)]