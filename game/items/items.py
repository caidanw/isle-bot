import enum
import math


class Item:
    def __init__(self, name, harvest_time):
        self.name = name.upper()
        self.harvest_time = harvest_time

        try:
            self.uid = get_uid_by_name(self.name)
        except KeyError:
            raise ValueError(f'Item "{name}" is not registered. Check ItemLookup(Enum)')


def get_uid_by_name(name):
    if isinstance(name, str):
        name = name.upper()  # want to get the right value
        return ItemLookup[name].value
    else:
        raise ValueError('name must be a string')


def get_name_by_uid(uid):
    if isinstance(uid, (int, float, bool)):
        return ItemLookup(int(uid)).name
    else:
        raise ValueError('id must be an int, float, or bool')


def _roundup(x):
    return int(math.ceil(x / 100.0)) * 100  # round number to the nearest 100


def get_by_uid(uid, new_object=True):
    name = get_name_by_uid(uid)
    name = name.title()  # need to make into CamelCase for item class name

    from game.items import harvested

    item_type_file = {
        100: harvested,
        # 100: tools
    }

    item_type = item_type_file.get(_roundup(uid))

    item_class = getattr(item_type, name)
    if new_object:
        return item_class()  # create a new instance of the class
    else:
        return item_class  # just return the class


def get_by_name(name, new_object=True):
    name = name.title()  # need to make into CamelCase for item class name
    uid = get_uid_by_name(name)

    from game.items import harvested

    item_type_file = {
        100: harvested,
        # 100: tools
    }

    item_type = item_type_file.get(_roundup(uid))

    item_class = getattr(item_type, name)
    if new_object:
        return item_class()  # create a new instance of the class
    else:
        return item_class  # just return the class


class ItemLookup(enum.Enum):
    """ Look up items based on their class name """

    """ Items that can be harvested or used in recipes, value represents harvest time. """

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

    """ Tools that can be crafted from harvested items. """

    # todo: convert tools to classes
    STONE_AXE = 100

    def __str__(self):
        return self.name
