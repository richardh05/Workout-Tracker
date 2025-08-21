from pandas import DataFrame

class InputHelper:
  @property
  def aliases(self) -> dict[str, list[str]]:
    aliases = {
        # 'day': ['d', 'days'],
        'exercise': ['exercises'],
        'set': ['sets'],
        'workout': ['workouts'],
        'reps': ["repetitions", 'repetition', 'rep'],

        'value': ['weight', 'wgt'],
        'note': ['notes'],
        'date': ['dte', 'dates', "day", "days"],
        'unit': ['units']
    }
    for key in aliases:
          aliases[key] = [key] + aliases[key]

    return aliases
  
  def sanitize_col_names(self , df: DataFrame) -> DataFrame:
      

  def sanitize_units(self, df: DataFrame) -> DataFrame:
    def sanitize_unit_rows(
            values: list[str],
            unit_labels: list[str],
            unit_cols: list[list[str]]

    ) -> tuple[list[float],str]:
        
    unit_aliases = self.aliases['unit']
    unit_cols = []

    # Loop over each alias and each column name directly
    for alias in unit_aliases:
        for col in df.columns:
            if alias in col:
                unit_cols.append(col)


      if unit_cols:
          print(f"Found unit column: {unit_cols}")
      else:
          print("No unit column found.")
  
  