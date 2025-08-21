from datetime import date
from typing import cast

import pandas as pd

from pylift.classes.day import Day
from pylift.classes.exercise_type import ExerciseType
from pylift.classes.set import Set
from pylift.classes.workout import Workout


class ValueParseError(Exception):
    """Raised when the value in a workout dataframe row cannot be parsed properly."""

    pass


class UnitParseError(Exception):
    """Raised when the unit in a workout dataframe row cannot be parsed properly."""

    pass


def parse_value_unit_columns(row: pd.Series) -> tuple[float, str]:
    """
    Parses the 'value' and 'unit' columns from a pandas DataFrame row.
    Parameters:
        row: A single row from a pandas DataFrame containing at least
                         'value' and 'unit' fields.
        unit_aliases: A mapping from canonical units to lists of aliases.

    Returns:
        A tuple containing the numeric value and canonical unit string.

    Raises:
        ValueUnitParseError: If the value is missing, not numeric, or the unit is unrecognized.
    """
    # Extract and validate the 'value'
    val = row["value"]
    if pd.isna(val):
        msg = "Missing or null 'value' column."
        raise ValueParseError(msg)

    try:
        num = float(val)
    except (TypeError, ValueError) as e:
        msg = f"Invalid numeric value: {row['value']}"
        raise ValueParseError(msg) from e

    # Extract and normalize the 'unit'
    if "unit" not in row or pd.isna(row["unit"]):
        msg = "Missing or null 'unit' column."
        raise UnitParseError(msg)

    unit_raw = str(row["unit"]).strip().lower()

    return num, unit_raw


# TODO: Refactor this to  load the unit from the settings file
def parse_inferred_unit(
    row: pd.Series,
    unit_aliases: dict[str, list[str]],
    exercise_types: list[ExerciseType],
) -> tuple[float, str]:
    """
    Parses the value from a pandas DataFrame row, inferring the unit as the ExerciseType's default unit.
    Parameters:
        row: A single row from a pandas DataFrame containing at least 'value' and 'unit' fields.
        unit_aliases: A mapping from canonical units to lists of aliases.

    Returns:
        A tuple containing the numeric value and canonical unit string.

    Raises:
        ValueUnitParseError: If the value i
    Returns:s missing, not numeric, or the unit is unrecognized.
    """
    # Check for 'value' field
    val = float(row["value"])
    if pd.isna(val):
        msg = "Missing or null 'value' column."
        raise ValueParseError(msg)

    # Try to parse the value
    try:
        num = float(val)
    except (TypeError, ValueError) as e:
        msg = f"Invalid numeric value: {row['value']}"
        raise ValueParseError(msg) from e

    # Check for 'exercise' field to determine default unit
    if pd.isna(row["exercise"]):
        msg = "Missing or null 'exercise' column."
        raise ValueParseError(msg)

    my_exercise_name = str(row["exercise"]).strip().lower()

    # Find matching ExerciseType by name
    for ex in exercise_types:
        if ex.name.strip().lower() == my_exercise_name:
            default_unit = ex.unit.strip().lower()
            # Normalize the unit if aliases exist
            for canonical, aliases in unit_aliases.items():
                if default_unit == canonical or default_unit in aliases:
                    return num, canonical
            return (num, default_unit)  # Return even if not in aliases
    msg = "No matching exercise type found"
    raise UnitParseError(msg)


def workout_from_dataframe(df: pd.DataFrame) -> Workout:
    exercise_type = df["Exercise"].iloc[0]
    note = "; ".join(map(str, df["Notes"].dropna())) or None
    sets = [Set(value=v, reps=r) for v, r in zip(df["Value"], df["Reps"], strict=True)]
    return Workout(exercise_type=exercise_type, sets=sets, note=note)


def days_from_dataframe(df: pd.DataFrame) -> list[Day]:
    df["Date"] = pd.to_datetime(df["Date"])

    days = []
    for date_val, df_day in df.groupby("Date"):
        ts = cast(pd.Timestamp, date_val)  # tell Pylance it's a Timestamp
        date_clean: date = ts.date()
        workouts = []

        boundaries = df_day["Exercise"].ne(df_day["Exercise"].shift()).cumsum()
        for _, df_ex in df_day.groupby(boundaries):
            workouts.append(workout_from_dataframe(df_ex))

        days.append(Day(date_clean, workouts))

    return days
