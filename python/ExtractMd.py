import MarkdownParser
from typing import List
from io import StringIO
import pandas

def extractMD(path: str) -> List[str]:
    mp = MarkdownParser.MarkdownParser()
    try:
        with open(path, 'r', encoding='utf-8') as f:
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

    except FileNotFoundError:
        return []
    except Exception as e:
        return []

    return days


myList = extractMD("/home/richard/Documents/Obsidian/Personal/02 Projects/Fitness/Exercise.md")
