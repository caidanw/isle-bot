from enum import Enum

from src.game.items.abstract_item import MaterialIndex


class Recipe(Enum):
    """ A blueprint of sorts for what materials are needed to make a craftable item,
    value represents the harvested materials needed.
    """

    WOOD_AXE = {MaterialIndex.WOOD: 5}
    WOOD_SWORD = {MaterialIndex.WOOD: 5}
    WOOD_SHIELD = {MaterialIndex.WOOD: 5, MaterialIndex.VINE: 5}

    STONE_AXE = {MaterialIndex.WOOD: 3, MaterialIndex.STONE: 2}
    STONE_SWORD = {MaterialIndex.WOOD: 2, MaterialIndex.STONE: 3}
    STONE_SHIELD = {MaterialIndex.VINE: 5, MaterialIndex.STONE: 5}

    def __str__(self):
        return self.name

    def needs_materials(self):
        return self.value

    def to_short_string(self):
        ingredients = []
        for material, amt in self.value.items():
            ingredients.append(f'{str(material)}: {str(amt)}')

        return f'[{", ".join(ingredients)}]'

    def to_extended_string(self):
        output = '```\n'

        header = self.name.replace('_', ' ') + ' RECIPE'
        output += header

        output += '\n' + '-' * len(header)

        for material, amt in self.value.items():
            name = str(material).ljust(10)
            amt = str(amt).zfill(3)
            output += f'\n{name} : {amt}'
        output += '\n```'

        return output
