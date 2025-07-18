from dataclasses import dataclass
import json
from json import dump, load
from pathlib import Path

from pylift.utils.dir import get_data_dir


@dataclass
class ExerciseType:
    name: str
    unit: str
    category: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "unit": self.unit,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ExerciseType":
        return ExerciseType(
            name=data["name"],
            unit=data["unit"],
            category=data["category"],
        )

    @classmethod
    def read(cls, filepath: Path) -> list["ExerciseType"]:
        """
        Read a list of ExerciseType from a JSON file.
        """
        with filepath.open() as f:
            data: list[dict] = json.load(f)
        return [cls.from_dict(et) for et in data]

    @staticmethod
    def save(et: "ExerciseType", filepath: Path = get_data_dir()) -> None:  # noqa: B008
        """
        Save a single ExerciseType to a JSON file. Merges with existing ExerciseType data if it already exists.
        """
        filename = filepath / "exercises.json"
        newdata: dict[str, str] = et.to_dict()
        with filename.open("w") as f:
            if not filename.exists():
                dump({"ExerciseTypes": [newdata]}, f, indent=4)
                return
            existing_data: list[dict[str, str]] = load(f)
            # Check if the exercise type already exists
            if not any(et["name"] == newdata["name"] for et in existing_data):
                existing_data.append(newdata)
            else:
                # Update the existing exercise type if it exists
                for i, existing_et in enumerate(existing_data):
                    if existing_et["name"] == newdata["name"]:
                        existing_data[i] = newdata
                        break
