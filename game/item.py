from collections import namedtuple


class Item:
    def __init__(self, name):
        self.name = name


ItemStack = namedtuple('ItemStack', ['item', 'amount'])
