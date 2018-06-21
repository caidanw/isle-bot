from enum import Enum


class Action(Enum):
    idle = 0
    harvesting = 1
    crafting = 2
    traveling = 3

    def __str__(self):
        return self.name
