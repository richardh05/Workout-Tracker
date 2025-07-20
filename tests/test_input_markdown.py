from pathlib import Path

import pytest

from pylift.classes.day import Day
from pylift.input.markdown import read_markdown
from tests.factories.day_factory import DayFactory

seeds = [42, 123, 456]


def cases(seeds: list[int]) -> list[tuple[str, list[Day]]]:
    factory = DayFactory(seeds[0])
    comparisons = [(factory.static_markdown(), factory.static_days())]
    for seed in seeds[1:]:
        factory = DayFactory(seed)
        r = factory.random_markdown()
        comparisons.append(r)
    return comparisons


@pytest.mark.parametrize("markdown, expected_days", cases(seeds))
def test_read_markdown(markdown, expected_days, tmp_path: Path) -> None:
    # Write the markdown to a temporary file
    with open(tmp_path / "test_markdown.md", "w", encoding="utf-8") as f:
        f.write(markdown)

    # Read the markdown file
    md_days = read_markdown(Path(tmp_path / "test_markdown.md"))

    for i in range(len(md_days)):
        day = expected_days[i]
        md_day = md_days[i]
        assert isinstance(md_day, Day), f"Expected Day instance, got {type(md_day)}"
        assert md_day.date == day.date, f"Expected date {day.date}, got {md_day.date}"
        assert len(md_day.workouts) == len(day.workouts), (
            f"Expected {len(day.workouts)} workouts, got {len(md_day.workouts)}"
        )
        for j in range(len(md_day.workouts)):
            assert md_day.workouts[j].exercise_type == day.workouts[j].exercise_type
            assert md_day.workouts[j].note == day.workouts[j].note
            assert len(md_day.workouts[j].sets) == len(day.workouts[j].sets)
            for k in range(len(md_day.workouts[j].sets)):
                assert md_day.workouts[j].sets[k] == day.workouts[j].sets[k]
