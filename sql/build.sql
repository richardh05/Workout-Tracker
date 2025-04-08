CREATE TABLE Day (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Date TEXT NOT NULL UNIQUE
) STRICT;

CREATE TABLE ExerciseType (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    ExerciseName TEXT NOT NULL UNIQUE,
    Unit TEXT NOT NULL,
    Category TEXT CHECK (Category IN ('Push', 'Pull', 'Legs', 'Cardio'))
) STRICT;

CREATE TABLE WorkoutItem (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    DayId INTEGER NOT NULL,
    ExerciseTypeId INTEGER NOT NULL,
    FOREIGN KEY (DayId) REFERENCES Day(Id),
    FOREIGN KEY (ExerciseTypeId) REFERENCES ExerciseType(Id)
) STRICT;

CREATE TABLE WorkoutSet (
    WorkoutItemId INTEGER NOT NULL,
    SetNo INTEGER NOT NULL,
    Reps INTEGER CHECK (Reps > 0),
    Value REAL CHECK (Value >= 0),
    Note TEXT,
    PRIMARY KEY (WorkoutItemId, SetNo),
    FOREIGN KEY (WorkoutItemId) REFERENCES WorkoutItem(Id)
) STRICT;