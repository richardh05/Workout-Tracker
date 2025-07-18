import sys
from typing import List, Optional
import pandas
import sqlite3
import DataClasses as c

class DatabaseConnector:
    def __init__(self, path:str):
        self.path = path

    def connect(self) -> sqlite3.Connection:
        try:
            conn = sqlite3.connect(self.path)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            sys.exit()
        
    def getIdByUnique(self, table:str, unique_cols_and_vals: dict):
        conn = self.connect()
        cursor = conn.cursor()
        try:
             # Construct WHERE clause for multiple columns
            where_clauses = [f"{col} = ?" for col in unique_cols_and_vals.keys()]
            sql_query = f"SELECT Id FROM {table} WHERE {' AND '.join(where_clauses)}"
            values = tuple(unique_cols_and_vals.values())
            cursor.execute(sql_query, values)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Database error during Id retrieval in {table} with unique values {unique_cols_and_vals}: {e}")
            return None
        
    def getExerciseTypeByName(self, name:str) -> Optional[c.ExerciseType]:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            sql_query = f"SELECT Name, Unit, Category FROM ExerciseType WHERE Name = ?"
            cursor.execute(sql_query, (name,))
            row = cursor.fetchone()
            if row:
                result = c.ExerciseType(row[0],row[1],row[2])
                return result
            else:
                return None
        except sqlite3.Error as e:
            print(f"Database error during ExerciseType retrieval with the name {name}: {e}")
            return None
        
    def readExerciseTypes(self) -> dict[int, c.ExerciseType]:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Name, Unit, Category FROM ExerciseType")
            rows = cursor.fetchall()
            # Create a dictionary keyed by ExerciseID
            result = {
                id: c.ExerciseType(name, unit, category)
                for name, unit, category in rows
            }
            return result
        except sqlite3.Error as e:
            print(f"Database error while reading ExerciseTypes: {e}")
            return {}
        finally:
            conn.close()

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
    
    def WriteExerciseTypeClass(self, x:c.ExerciseType):
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

    def writeWorkoutClass(self, w:c.Workout, DayId:int):
        conn = self.connect()
        # exercise types ripped from markdown won't have id, unit or category
        w.exerciseType.id = self.getIdByUnique("ExerciseType", dict(Name = w.exerciseType.name))
        checkedExerciseType = self.getExerciseTypeByName(w.exerciseType.name)
        print(checkedExerciseType)
        print(w.exerciseType.name)
        if (checkedExerciseType == None):
            checkedExerciseType = ExerciseTypeDialogue(w.exerciseType.name)
            self.WriteExerciseTypeClass(checkedExerciseType)
            checkedExerciseType.id = self.getIdByUnique("ExerciseType",dict (Name = checkedExerciseType.name)) 
        self._insert(conn, "Workout", "DayId,ExerciseTypeId,Note", (DayId,checkedExerciseType.id,w.note))

        w.id = self.getIdByUnique("Workout", dict(DayId=DayId, ExerciseTypeId=w.exerciseType.id, Note=w.note))
        print(w)
        if w.id != None:
            self.writeWorkoutSets(w.sets, w.id)
        else:
            print("Error: writeWorkoutClass() wants to write WorkoutSets with no Id!")
            sys.exit()
        conn.close()

    def writeDayClass(self, d:c.Day):
        conn = self.connect()
        self._insert(conn, "Day", "Date", (d.date,))
        conn.close()
        d.id = self.getIdByUnique("Day",dict(Date=d.date))
        if d.id == None:
            print("Error: writeDayClass() is not inserting new Days correctly, as the Id lookup fails")
            sys.exit()
        for w in d.workouts:
            self.writeWorkoutClass(w, d.id)