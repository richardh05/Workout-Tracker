from pylift.classes.exercise_type import ExerciseType


def exercise_type_dialogue(exercise: str) -> ExerciseType:
    print(
        f"It seems that '{exercise}' doesn't exist in your database. If you'd like to add it, hit enter. Otherwise, type anything else to rename it."
    )
    user_input = input("> ").strip()
    x_name: str
    if not user_input:  # User hit enter (empty string)
        print(f"Adding '{exercise}' to the database.")
        x_name = exercise
    else:
        print(f"Renaming '{exercise}' to '{user_input}'.")
        x_name = user_input
    x_unit: str = ""
    while not x_unit:
        print(
            "Please enter a unit (Kg, Km, etc) that your exercise will be measured with. If this doesn't apply, enter 'N/A'."
        )
        x_unit = input("> ").strip()
    x_category: str = ""
    while not x_category:
        print("Finally, please specify the category (Push, Pull, Legs or Cardio).")
        x_category = input("> ").strip()
    return ExerciseType(x_name, x_unit, x_category)
