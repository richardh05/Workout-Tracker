from dataclasses import dataclass
from datetime import date
from random import Random, randint


@dataclass
class Factory:
    """
    Base class for factories.
    """

    seed: int = randint(0, 10000)

    def __post_init__(self) -> None:
        self.r = Random(self.seed)

    def random_float(self, mini: float = 0.0, maxi: float = 100.0) -> float:
        return self.r.uniform(mini, maxi)

    def random_date(self) -> date:
        return date(self.r.randint(1970, 2070), self.r.randint(1, 12), self.r.randint(1, 28))

    def random_date_str(self) -> tuple[date, str]:
        d = self.random_date()
        ds = d.strftime("%Y-%m-%d")
        return (d, ds)
