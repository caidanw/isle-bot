from enum import Enum

from game.items.item import ItemLookup


class Recipe(Enum):
    """ A blueprint of sorts for what items are needed to make a craftable item,
    value represents the harvested items needed.
    """

    # tools
    stone_axe = {ItemLookup['wood']: 2, ItemLookup['stone']: 1}

    def needs_items(self):
        return self.value

    def to_string(self):
        output = '```\n'
        header = self.name.title().replace('_', ' ') + ' Recipe'
        output += header
        output += '\n' + '-' * len(header)
        for item, amt in self.value.items():
            name = item.name.ljust(10)
            amt = str(amt).zfill(3)
            output += f'\n{name} : {amt}'
        output += '\n```'
        return output
