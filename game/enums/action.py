from enum import Enum


class Action(Enum):
    IDLE = 0
    HARVESTING = 1
    CRAFTING = 2
    TRAVELING = 3

    def __str__(self):
        return self.name
