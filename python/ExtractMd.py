import MarkdownLog
from typing import List
import pandas
import sqlite3

SQLitePath:str = "/home/richard/Documents/gym"

def connectDb() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(SQLitePath)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
    return None

def writeDay(date:str, conn:sqlite3.Connection):
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

def getIdByUnique(conn:sqlite3.Connection, table:str, uniqueColName, uniqueVal):
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

def writeWorkoutAndSets(Date:str, ExerciseType:str, Note:str, conn:sqlite3.Connection):
    DayId = getIdByUnique(conn,"Day","Date",Date)
    ExerciseId = getIdByUnique(conn,"ExerciseType","Name",ExerciseType)


myMarkdown = MarkdownLog.MarkdownLog("/home/richard/Documents/Obsidian/Personal/02 Projects/Fitness/Exercise.md")
for d in myMarkdown.days:
    print(d.date)