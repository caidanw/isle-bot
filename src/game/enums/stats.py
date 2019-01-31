from enum import Enum


class Stats(Enum):
    VIGOR = 0
    STRENGTH = 1
    DEXTERITY = 2
    FORTITUDE = 3

    def __str__(self):
        return self.name


STAT_NAMES = [str(stat).lower() for stat in Stats.__members__]
