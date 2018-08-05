import enum


class Item:
    def __init__(self, name, harvest_time):
        self.name = name
        self.harvest_time = harvest_time


class ItemLookup(enum.Enum):
    """ Look up items based on their class name """

    from game.items.harvested.field import Grass, Wheat
    from game.items.harvested.forest import Leaf, Wood, Mushroom
    from game.items.harvested.quarry import Stone, Iron
    from game.items.harvested.swamp import Clay, Vine

    """ Items that can be harvested or used in recipes, value represents harvest time. """

    # forest
    WOOD = Wood()
    MUSHROOM = Mushroom()
    LEAF = Leaf()

    # quarry
    STONE = Stone()
    IRON = Iron()

    # swamp
    CLAY = Clay()
    VINE = Vine()

    # field
    GRASS = Grass()
    WHEAT = Wheat()

    """ Tools that can be crafted from harvested items. """

    # todo: convert tools to classes
    # STONE_AXE = StoneAxe

    def __str__(self):
        return self.name
