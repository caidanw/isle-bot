from enum import Enum


class Item:
    def __init__(self, name, harvest_time):
        self.name = name
        self.harvest_time = harvest_time


class ItemLookup(Enum):
    """ Look up items based on their class name """

    from game.items.harvested.field import Grass, Wheat
    from game.items.harvested.forest import Leaf, Wood, Mushroom
    from game.items.harvested.quarry import Stone, Iron
    from game.items.harvested.swamp import Clay, Vine

    """ Items that can be harvested or used in recipes, value represents harvest time. """

    # forest
    wood = Wood
    mushroom = Mushroom
    leaf = Leaf

    # quarry
    stone = Stone
    iron = Iron

    # swamp
    clay = Clay
    vine = Vine

    # field
    grass = Grass
    wheat = Wheat

    """ Tools that can be crafted from harvested items. """

    # todo: convert tools to classes
    # stone_axe = StoneAxe
