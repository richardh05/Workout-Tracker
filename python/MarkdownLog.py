from typing import List
from io import StringIO
import pandas
import DataClasses as Dc

class MarkdownLog:
    def __init__(self, path:str):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.markdown = f.readlines()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error: File not found at {path}") from e
        except Exception as e:
            raise Exception(f"An error occurred while reading {path}: {e}") from e

    def _seperateByHeader(self, mdFile: List[str], header: str) -> List[str]:
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

    def _getFirstLine (self, block: str, header: str) -> str:
        lines = block.splitlines()
        if lines and lines[0].startswith(header):
            return lines[0][len(header):].strip()
        else:
            return ""

    def _getNote(self, exercise: str) -> str:
        lines = exercise.splitlines()
        if len(lines) > 1 and lines[0].startswith("## "):
            note_line = lines[1].strip()
            for i in range(2, len(lines)):
                if lines[i].startswith("|"):
                    return note_line
            # If no '|' line is found, return the line after the header
            return note_line
        return ""

    def _getMarkdownTable(self, markdown: str) -> str:
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
        
    def _MarkdownToDataframe(self, markdown: str) -> pandas.DataFrame:
        try:
            df = pandas.read_csv(
                StringIO(markdown),
                sep='|',
                skipinitialspace=True,
                header=0,
                index_col=False
            )
            df = df.dropna(axis=1,how='all') #remove NaN columns
            df = df.dropna(axis=0,how='all') #remove NaN rows
            df = df.iloc[1:] #remove row 0
            df.columns = df.columns.str.strip()  # Remove leading/trailing whitespace from column names
            df['Reps'] = df['Reps'].astype(int)
            df['Value'] = df['Value'].astype(float)
            return df
        except Exception as e:
            print(f"Error parsing Markdown table with pandas: {e}")
            return pandas.DataFrame()
        
    @property
    def days(self) -> List[Dc.Day]:
        days:List[Dc.Day] = []
        h1blocks = self._seperateByHeader(self.markdown,"# ")
        for b1 in h1blocks:
            date = self._getFirstLine(b1,"# ")
            h2blocks = self._seperateByHeader(b1.splitlines(),"## ")
            workouts:List[Dc.Workout] = []
            for b2 in h2blocks: 
                exerciseTypeName = self._getFirstLine(b2,"## ")
                mdSets = self._getMarkdownTable(b2)
                dfSets = self._MarkdownToDataframe(mdSets)
                note = self._getNote(b2)
                exerciseType = Dc.ExerciseType(None,exerciseTypeName,"","")
                myWorkout = Dc.Workout(None,exerciseType, dfSets, note)
                workouts.append(myWorkout)
            myDay = Dc.Day(None,date, workouts)
            days.append(myDay)
        return days

