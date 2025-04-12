import MarkdownLog
from typing import List
import pandas
import sqlite3
import DataClasses as Dc

class DatabaseConnector:
    def __init__(self, path:str):
        self.path = path

    def connect(self) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(self.path)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            return None
        
    def getIdByUnique(self, table:str, uniqueColName:str, uniqueVal):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            sql_query = f"SELECT Id FROM {table} WHERE {uniqueColName} = ?"
            cursor.execute(sql_query, (uniqueVal,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Database error during Id retrieval in {table} with the unique value {uniqueColName}={uniqueVal}: {e}")
            return None

class DatabaseWriter(DatabaseConnector):
    def __init__(self, path):
        super().__init__(path)

    def _insert(self, conn, table:str, colNames:str, values:tuple):
        cursor = conn.cursor()
        try:
            # Split the colNames string into a list of individual column names
            columns = [col.strip() for col in colNames.split(',')]
            num_columns = len(columns)

            # Create the appropriate number of placeholders (?, ?, ...)
            placeholders = ', '.join(['?'] * num_columns)

            # Construct the SQL query with the dynamic placeholders
            sql_query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

            # Execute the query with the tuple of values
            cursor.execute(sql_query, values)
            conn.commit()
            print(f"Successfully added '{values}' to {table} (columns: {', '.join(columns)})")
        except sqlite3.IntegrityError as e:
            print(f"Error: {table} with values '{values}' likely already exists. ({e})")
            conn.rollback()
        except sqlite3.Error as e:
            print(f"Database error during {table} insertion: {e}")
            conn.rollback()        

    def ExerciseTypeDialogue(self, exercise:str) -> Dc.ExerciseType:
        print(f"It seems that '{exercise}' doesn't exist in your database. If you'd like to add it, hit enter. Otherwise, type anything else to rename it.")
        user_input = input("> ").strip()
        xName:str
        if not user_input:  # User hit enter (empty string)
            print(f"Adding '{exercise}' to the database.")
            xName = exercise
        else:
            print(f"Renaming '{exercise}' to '{user_input}'.")
            xName = user_input
        xUnit:str = None
        while not xUnit:
            print(f"Please enter a unit (Kg, Km, etc) that your exercise will be measured with. If this doesn't apply, enter 'N/A'.")
            xUnit = input("> ").strip()
        xCategory:str = None
        while not xCategory:
            print(f"Finally, please specify the category (Push, Pull, Legs or Cardio).")
            xCategory = input("> ").strip()
        x = Dc.ExerciseType(xName,xUnit,xCategory)
        return x
    
    def WriteExerciseTypeClass(self, x:Dc.ExerciseType):
        conn = self.connect()
        self._insert(conn, "ExerciseType", "Name,Unit,Category", (x.name,x.unit,x.category))
        conn.close()

    def writeWorkoutSets(self, s:pandas.DataFrame, workoutId:int):
        conn = self.connect()
        for row in s.itertuples():
            index = row[0]  # Index
            value = row.Value
            reps = row.Reps
            self._insert(conn,"WorkoutSet","WorkoutId,SetNo,Value,Reps", 
                         (workoutId, index, value, reps))
        conn.close()

    def writeWorkoutClass(self, w:Dc.Workout, DayId:int):
        conn = self.connect()
        ExerciseId = self.getIdByUnique("ExerciseType","Name", w.exerciseType)
        if (ExerciseId == None):
            x:Dc.ExerciseType = self.ExerciseTypeDialogue(w.exerciseType)
            self.WriteExerciseTypeClass(x)
            ExerciseId = self.getIdByUnique("ExerciseType","Name", w.exerciseType)
        self._insert(conn, "Workout", "DayId,ExerciseTypeId,Note", (DayId,ExerciseId,w.note))
        self.writeWorkoutSets(w.sets, ExerciseId)
        conn.close()

    def writeDayClass(self, d:Dc.Day):
        conn = self.connect()
        self._insert(conn, "Day", "Date", (d.date,))
        conn.close()
        DayId = self.getIdByUnique("Day","Date",d.date)
        for w in d.workouts:
            self.writeWorkoutClass(w, DayId)


