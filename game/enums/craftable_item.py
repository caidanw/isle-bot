from enum import Enum


class CraftableItem(Enum):
    """ Items that can be crafted from harvested items using a recipe, value represents durability. """

    # tools
    stone_axe = 10

    def durability(self):
        return self.value
