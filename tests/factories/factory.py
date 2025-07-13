from random import randint,Random
from datetime import date
from dataclasses import dataclass

@dataclass
class Factory:
    """
    Base class for factories.
    """
    seed: int = randint(0, 10000)

    def __post_init__(self):
      self.r = Random(self.seed)

    def random_float(self, min: float = 0.0, max: float = 100.0) -> float:
      return self.r.uniform(min, max)

    def random_date(self) -> date:
      # r = Random(request.param)
      return date(
        self.r.randint(1970,2070), 
        self.r.randint(1, 12), 
        self.r.randint(1, 28))
    
    def random_date_str(self) -> dict[str, date|str]:
      d = self.random_date()
      ds = d.strftime("%Y-%m-%d")
      return {"date":d, "str":ds}
    
