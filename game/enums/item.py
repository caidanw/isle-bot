from collections import namedtuple
from aenum import Enum, NoAlias


class Item(Enum):
    """ Items that can be harvested or used in recipes, value represents harvest time. """

    _settings_ = NoAlias  # needed so we don't accidentally get a different item

    # forest
    wood = 5
    mushroom = 4
    leaf = 2

    # quarry
    stone = 4
    iron = 12

    # swamp
    clay = 6
    vine = 4

    # field
    grass = 2
    wheat = 6

    def harvest_time(self):
        return self.value
