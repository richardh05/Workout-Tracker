from io import StringIO
from pathlib import Path

from pandas import DataFrame, read_csv, to_datetime
from pandas.errors import ParserError

from pylift.classes.day import Day
from pylift.classes.set import Set
from pylift.classes.workout import Workout


def _get_first_line(block: str, header: str) -> str:
    lines = block.splitlines()
    if lines and lines[0].startswith(header):
        return lines[0][len(header) :].strip()
    return ""


def _seperate_by_header(md_file: list[str], header: str) -> list[str]:
    h_blocks: list[str] = []
    current_block: str = ""

    for line in md_file:
        line = line.strip()  # noqa: PLW2901
        if line.startswith(header):
            if current_block:
                h_blocks.append(current_block.strip())
            current_block = line + "\n"  # Start a new block with the heading
        elif current_block:  # Only add content if we are within a header's block
            current_block += line + "\n"

    if current_block:
        h_blocks.append(current_block.strip())
    return h_blocks


def _parse_markdown_table(md_table: str) -> list[Set]:
    def _markdown_to_dataframe(markdown: str) -> DataFrame:
        try:
            df = read_csv(
                StringIO(markdown),
                sep="|",
                skipinitialspace=True,
                header=0,
                index_col=False,
            )
        except ParserError as e:
            msg = f"Error parsing Markdown table with pandas: {e}"
            raise ValueError(msg) from e
        else:
            df = df.dropna(axis=1, how="all")  # remove NaN columns
            df = df.dropna(axis=0, how="all")  # remove NaN rows
            df = df.iloc[1:]  # remove row 0
            df.columns = df.columns.str.strip() # Remove leading/trailing whitespace from column names
            df["Reps"] = df["Reps"].astype(int)
            df["Value"] = df["Value"].astype(float)
            return df

    def _get_sets(df: DataFrame) -> list[Set]:
        try:
            sets: list[Set] = []
            for _index, row in df.iterrows():
                reps = row["Reps"]
                value = row["Value"]
                my_set = Set(reps, value)
                sets.append(my_set)
        except ParserError as e:
            msg = f"Failed to parse Markdown table: {e}"
            raise ValueError(msg) from e
        else:
            return sets

    md_df = _markdown_to_dataframe(md_table)
    return _get_sets(md_df)


def parse_h2_block(block: str) -> Workout:
    def _get_note(exercise: str) -> str:
        lines = exercise.splitlines()
        if len(lines) > 1 and lines[0].startswith("## "):
            note_line = lines[1].strip()
            for i in range(2, len(lines)):
                if lines[i].startswith("|"):
                    return note_line
            # If no '|' line is found, return the line after the header
            return note_line
        return ""

    def _get_markdown_table(markdown: str) -> str:
        lines = [s.strip() for s in markdown.splitlines()]
        table_lines = []
        in_table = False

        for line in lines:
            if line.startswith("|"):
                in_table = True
                table_lines.append(line)
            elif in_table and not line.startswith("|") and table_lines:
                break

        if table_lines:
            return "\n".join(table_lines)
        return ""

    exercise_type_name = _get_first_line(block, "## ")
    md_sets = _get_markdown_table(block)
    sets = _parse_markdown_table(md_sets)
    note = _get_note(block)
    return Workout(exercise_type_name, sets, note)


def read_markdown(path: Path) -> list[Day]:
    def _init(path: Path) -> list[str]:
        try:
            with path.open() as f:
                return f.readlines()
        except FileNotFoundError as e:
            msg = f"Error: File not found at {path}"
            raise FileNotFoundError(msg) from e

    markdown = _init(path)
    days: list[Day] = []
    h1blocks = _seperate_by_header(markdown, "# ")
    for b1 in h1blocks:
        date_str = _get_first_line(b1, "# ")
        try:
            date = to_datetime(date_str).date()
        except ValueError as e:
            print(f"Error parsing date '{date_str}': {e}")
            continue
        h2blocks = _seperate_by_header(b1.splitlines(), "## ")
        workouts: list[Workout] = []
        for b2 in h2blocks:
            my_workout = parse_h2_block(b2)
            workouts.append(my_workout)
        my_day = Day(date, workouts)
        days.append(my_day)
    return days
