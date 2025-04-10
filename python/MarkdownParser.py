from typing import List
from io import StringIO
import pandas

class MarkdownParser:
    def __init__(self, path:str):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.markdown = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File not found at {path}") from e
        except Exception as e:
            raise Exception(f"An error occurred while reading {path}: {e}") from e

    def __seperateByHeader(self, mdFile: str, header: str) -> List[str]:
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
    
    @property
    def days(self) -> str:
        return self.__seperateByHeader(self.markdown,"# ")


    def getFirstLine (self, block: str, header: str) -> str:
        lines = block.splitlines()
        if lines and lines[0].startswith(header):
            return lines[0][len(header):].strip()
        else:
            return ""

    def getNote(self, exercise: str) -> str:
        lines = exercise.splitlines()
        if len(lines) > 1 and lines[0].startswith("## "):
            note_line = lines[1].strip()
            for i in range(2, len(lines)):
                if lines[i].startswith("|"):
                    return note_line
            # If no '|' line is found, return the line after the header
            return note_line
        return ""

    def getMarkdownTable(self, markdown: str) -> str:
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
        
    def MarkdownToDataframe(self, markdown: str) -> pandas.DataFrame:
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
            return df.iloc[1:] #remove row 0
        except Exception as e:
            print(f"Error parsing Markdown table with pandas: {e}")
            return pandas.DataFrame()