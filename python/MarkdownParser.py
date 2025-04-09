from typing import List
from io import StringIO
import pandas

def seperateByHeader(mdFile: str, header: str) -> List[str]:
    hBlocks: List[str] = []
    current_block: str = ""

    for line in mdFile:
        line = line.strip()
        if line.startswith(header):
            if current_block:
                hBlocks.append(current_block.strip())
            current_block = line + "\n"  # Start a new block with the heading
        elif current_block:  # Only add content if we are within a header's block
            current_block += line + "\n"

    if current_block:
        hBlocks.append(current_block.strip())
    return hBlocks


def getFirstLine (block: str, header: str) -> str:
    lines = block.splitlines()
    if lines and lines[0].startswith(header):
        return lines[0][len(header):].strip()
    else:
        return ""

def getNote(exercise: str) -> str:
    lines = exercise.splitlines()
    if len(lines) > 1 and lines[0].startswith("## "):
        note_line = lines[1].strip()
        for i in range(2, len(lines)):
            if lines[i].startswith("|"):
                return note_line
        # If no '|' line is found, return the line after the header
        return note_line
    return ""

def getMarkdownTable(markdown: str) -> str:
    lines = markdown.splitlines()
    table_lines = []
    in_table = False

    for line in lines:
        line = line.strip()
        if not in_table and line.startswith("|"):
            in_table = True
            table_lines.append(line)
        elif in_table and line.startswith("|"):
            table_lines.append(line)
        elif in_table and not line.startswith("|") and table_lines:
            # Stop if we were in a table and encounter a non-pipe line
            break

    if table_lines:
        return "\n".join(table_lines)
    else:
        return ""
    
def MarkdownToDataframe(markdown: str) -> pandas.DataFrame:
    try:
        # Use StringIO to treat the string as a file
        df = pandas.read_csv(
            StringIO(markdown),
            sep='|',
            skipinitialspace=True,
            header=0,
            index_col=False
        ).dropna(axis=1, how='all'
        ).iloc[1:] #remove row 0
        return df
    except Exception as e:
        print(f"Error parsing Markdown table with pandas: {e}")
        return pandas.DataFrame()


def extractMD(path: str) -> List[str]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            days = seperateByHeader(f.readlines(),"# ")
            for day in days:
                 date = getFirstLine(day,"# ")
                 exercises = seperateByHeader(day.splitlines(),"## ")
                 for e in exercises: 
                    exercise_type = getFirstLine(e,"## ")
                    note = getNote(e)
                    mdTable = getMarkdownTable(e)
                    df = MarkdownToDataframe(mdTable)
                    print(df)

    except FileNotFoundError:
        return []
    except Exception as e:
        return []

    return days

myList = extractMD("/home/richard/Documents/Obsidian/Personal/02 Projects/Fitness/Exercise.md")