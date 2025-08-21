class InputHelper:
    @property
    def aliases(self) -> dict[str, list[str]]:
        aliases = {
            "day": ["days"],
            "exercise": ["exercises"],
            "set": ["sets"],
            "workout": ["workouts"],
            "reps": ["repetitions", "repetition", "rep"],
            "value": ["weight", "wgt"],
            "note": ["notes"],
            "date": ["dte", "dates", "day", "days"],
            "unit": ["units"],
        }
        for key, values in aliases.items():
            aliases[key] = [key, *values]

        return aliases
