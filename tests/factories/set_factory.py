from tests.factories.factory import Factory
from pylift.classes.set import Set

class SetFactory(Factory):
  def random_set(self) -> Set:
    return Set(
      reps=self.r.randint(1, 20),
      value=self.random_float(0.0, 200.0)
    )
  
  def random_sets(self, count: int|None = None) -> list[Set]:
    if count is None: 
      count = self.r.randint(1, 6)
    return [self.random_set() for _ in range(count)]