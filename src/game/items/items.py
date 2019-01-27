import enum

from discord import User


class Item:
    def __init__(self, name, consumable=False):
        self.name = name.upper()
        self.consumable = consumable

        try:
            if isinstance(self, Material):
                self.uid = get_material_uid(self.name)
            elif isinstance(self, Living):
                self.uid = get_living_uid(self.name)
            elif isinstance(self, Crafted):
                self.uid = get_crafted_uid(self.name)
        except KeyError:
            raise ValueError(f'Item "{name}" is not registered. Check ItemIndex(Enum)')

    @property
    def can_consume(self):
        return self.consumable

    async def consume(self, client, user: User):
        pass  # leave blank as child classes will be able to define the exact behavior


class Material(Item):
    def __init__(self, name, harvest_time, consumable=False):
        super().__init__(name, consumable)
        self.harvest_time = harvest_time


class Living(Material):
    def __init__(self, name, harvest_time):
        super().__init__(name, harvest_time, consumable=True)


class Crafted(Item):
    def __init__(self, name, durability):
        super().__init__(name)
        self.durability = durability


def get_material_uid(name):
    if isinstance(name, str):
        try:
            name = name.upper()  # want to get the right value
            return MaterialIndex[name].value
        except KeyError:
            return None
    else:
        raise ValueError('material name must be a string')


def get_living_uid(name):
    if isinstance(name, str):
        try:
            name = name.upper()  # want to get the right value
            return LivingIndex[name].value
        except KeyError:
            return None
    else:
        raise ValueError('material name must be a string')


def get_crafted_uid(name):
    if isinstance(name, str):
        try:
            name = name.upper()  # want to get the right value
            return CraftedIndex[name].value
        except KeyError:
            return None
    else:
        raise ValueError('material name must be a string')


def get_name_by_uid(uid):
    if isinstance(uid, int):
        return ItemIndex(int(uid)).name
    else:
        raise ValueError('id must be an integer')


def get_class_type(name):
    # make upper and replace space with underscore
    name = name.upper()
    name = name.replace(' ', '_')

    material = list(MaterialIndex.__members__.keys())
    living = list(LivingIndex.__members__.keys())
    crafted = list(CraftedIndex.__members__.keys())

    class_type = None

    if name in material:
        class_type = Material
    elif name in living:
        class_type = Living
    elif name in crafted:
        class_type = Crafted

    return class_type


def get_by_name(name, new_object=True):
    class_type = get_class_type(name)
    if class_type is None:
        return None

    from src.game.items import crafted
    from src.game.items import material
    from src.game.items import living
    item_file = {
        Material: material,
        Living: living,
        Crafted: crafted,
    }

    # need to make into CamelCase for item class name
    name = name.title()
    name = name.replace(' ', '')
    name = name.replace('_', '')

    item_class = getattr(item_file.get(class_type), name)

    if new_object:
        return item_class()  # create a new instance of the class
    else:
        return item_class  # just return the class


class ItemIndex(enum.Enum):
    """ Look up items based on their class name """
    def __str__(self):
        return self.name


class MaterialIndex(ItemIndex):
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


class LivingIndex(ItemIndex):
    """ Living things that don't have much of a purpose other than to be eaten or traded. """

    FAIRY = 1


class CraftedIndex(ItemIndex):
    """ Items that can be crafted from harvested materials. """

    STONE_AXE = 1
    STONE_SWORD = 2
    STONE_SHIELD = 3
