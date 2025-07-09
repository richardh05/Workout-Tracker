from pylift.classes.exercise_type import ExerciseType

def ExerciseTypeDialogue(exercise:str) -> ExerciseType:
    print(f"It seems that '{exercise}' doesn't exist in your database. If you'd like to add it, hit enter. Otherwise, type anything else to rename it.")
    user_input = input("> ").strip()
    xName:str
    if not user_input:  # User hit enter (empty string)
        print(f"Adding '{exercise}' to the database.")
        xName = exercise
    else:
        print(f"Renaming '{exercise}' to '{user_input}'.")
        xName = user_input
    xUnit:str = ""
    while not xUnit:
        print(f"Please enter a unit (Kg, Km, etc) that your exercise will be measured with. If this doesn't apply, enter 'N/A'.")
        xUnit = input("> ").strip()
    xCategory:str = ""
    while not xCategory:
        print(f"Finally, please specify the category (Push, Pull, Legs or Cardio).")
        xCategory = input("> ").strip()
    x = ExerciseType(xName,xUnit,xCategory)
    return x