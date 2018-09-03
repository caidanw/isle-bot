import enum
import math

from discord import User


class Item:
    def __init__(self, name, harvest_time, consumable=False):
        self.name = name.upper()
        self.harvest_time = harvest_time
        self.consumable = consumable

        try:
            self.uid = get_uid_by_name(self.name)
        except KeyError:
            raise ValueError(f'Item "{name}" is not registered. Check ItemLookup(Enum)')

    @property
    def can_consume(self):
        return self.consumable

    async def consume(self, client, user: User):
        pass  # leave blank as child classes will be able to define the exact behavior


def get_uid_by_name(name):
    if isinstance(name, str):
        name = name.upper()  # want to get the right value
        try:
            return ItemLookup[name].value
        except KeyError:
            return None
    else:
        raise ValueError('name must be a string')


def get_name_by_uid(uid):
    if isinstance(uid, int):
        return ItemLookup(int(uid)).name
    else:
        raise ValueError('id must be an integer')


def _roundup(x):
    return int(math.ceil(x / 100.0)) * 100  # round number to the nearest 100


def get_by_name(name, new_object=True):
    name = name.title()  # need to make into CamelCase for item class name
    uid = get_uid_by_name(name)

    if uid is None:
        return None

    from game.items import harvested, living

    item_type_file = {
        100: harvested,
        200: living,
        # 300: tools
    }

    item_type = item_type_file.get(_roundup(uid))

    item_class = getattr(item_type, name)

    if new_object:
        return item_class()  # create a new instance of the class
    else:
        return item_class  # just return the class


class ItemLookup(enum.Enum):
    """ Look up items based on their class name """

    """ Materials that can be harvested or used in recipes, value represents harvest time. """

    # forest
    WOOD = 1
    MUSHROOM = 2
    LEAF = 3

    # quarry
    STONE = 4
    IRON = 5

    # swamp
    CLAY = 6
    VINE = 7

    # field
    GRASS = 8
    WHEAT = 9

    """ Living things that don't have much of a purpose other than to be eaten or traded. """

    FAIRY = 101

    """ Tools that can be crafted from harvested materials. """

    # todo: convert tools to classes
    STONE_AXE = 200

    def __str__(self):
        return self.name
