import MarkdownParser
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

def writeDb(f):
    mp = MarkdownParser.MarkdownParser()
    days = mp.seperateByHeader(f.readlines(),"# ")
    for day in days:
        date = mp.getFirstLine(day,"# ")
        exercises = mp.seperateByHeader(day.splitlines(),"## ")
        for e in exercises: 
            exercise_type = mp.getFirstLine(e,"## ")
            note = mp.getNote(e)
            mdTable = mp.getMarkdownTable(e)
            df = mp.MarkdownToDataframe(mdTable)
            print(df)

def openMd(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            writeDb(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        return []



myList = openMd("/home/richard/Documents/Obsidian/Personal/02 Projects/Fitness/Exercise.md")
