# Introduction
Simple Python and SQL code to populate my exercise database with records, and (soon) generate graphs and statistics from the database. The data is stored in an SQLite database with the following layout:

```mermaid
erDiagram
    ExerciseType ||--o{ Workout : includes
    Workout }o--|| Day : performed_in
    WorkoutSet }|--|| Workout : belongs_to
    Day {
        INTEGER DayId PK
        TEXT Date
    }
    ExerciseType {
        INTEGER ExerciseID PK
        TEXT Name
        TEXT Unit
        TEXT Category 
    }
    Workout {
        INTEGER WorkoutId PK
        INTEGER DayId FK
        INTEGER ExerciseId FK
        TEXT Note
    }
    WorkoutSet {
        INTEGER WorkoutId PK,FK
        INTEGER SetNo PK
        INTEGER Reps 
        REAL Value
    }
```