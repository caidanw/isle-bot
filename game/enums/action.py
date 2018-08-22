from enum import Enum


class Action(Enum):
    IDLE = 0
    HARVESTING = 1
    CRAFTING = 2
    TRAVELING = 3
    FIGHTING = 4
    EATING = 5

    def __str__(self):
        return self.name
