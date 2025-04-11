import MarkdownLog
from typing import List
import pandas
import sqlite3
import DataClasses as Dc

SQLitePath:str = "/home/richard/Documents/gym"

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
        conn = self.connect
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

    def _insert(conn, table:str, colNames:str, values:tuple):
        cursor = conn.cursor()
        try:
            sql_query = f"INSERT INTO {table} ({colNames}) VALUES (?)"
            cursor.execute(sql_query, values)
            conn.commit()
            print(f"Successfully added '{values}' to {table}")
        except sqlite3.IntegrityError as e:
            print(f"Error: {table} with values '{values}' likely already exists. ({e})")
            conn.rollback()
        except sqlite3.Error as e:
            print(f"Database error during insertion: {e}")
            conn.rollback()        

    def WriteExerciseTypeClass(self, x:Dc.ExerciseType):
        conn = self.connect()
        self._insert(conn, "ExerciseType", "Name,Unit,Category", (x.name,x.unit,x.category))
        conn.close()
    

    def ExerciseTypeDialogue(exercise:str):
        print(f"It seems that '{exercise}' doesn't exist in your database. If you'd like to add it, hit enter. Otherwise, type anything else to rename it")


    def writeDayClass(self, myDay:Dc.Day):
        conn = self.connect()
        self._insert(conn, "Day", "Date", (myDay.date,))
        DayId = self.getIdByUnique("Day","Date",myDay.date)
        for w in myDay.workouts:
            ExerciseId = self.getIdByUnique("ExerciseType","Name", w.exercise_type)
            if (ExerciseId == None):
                self.ExerciseTypeDialogue(w.exercise_type)


