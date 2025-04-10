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
            print(f"Database error during Day ID retrieval: {e}")
            return None

class DatabaseWriter(DatabaseConnector):
    def __init__(self, path):
        super().__init__(path)

    def insertDay(date:str, conn:sqlite3.Connection):
        cursor = conn.cursor()
        try:
            sql_query = "INSERT INTO Day (Date) VALUES (?)"
            cursor.execute(sql_query, (date,))
            conn.commit()
            print(f"Successfully added date '{date}' to the Day table.")
        except sqlite3.IntegrityError as e:
            print(f"Error: Date '{date}' already exists. ({e})")
            conn.rollback()
        except sqlite3.Error as e:
            print(f"Database error during insertion: {e}")
            conn.rollback()

    def writeDayClass(self, myDay:Dc.Day):
        self.insertDay(myDay.date)
        DayId = self.getIdByUnique("Day","Date",myDay.date)
        ExerciseId = self.getIdByUnique("ExerciseType","Name",myDay.ExerciseType)


