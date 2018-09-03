from enum import Enum


class CraftableItem(Enum):
    """ Items that can be crafted from harvested materials using a recipe, value represents durability. """

    # tools
    STONE_AXE = 10

    def durability(self):
        return self.value
