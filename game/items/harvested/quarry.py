from game.items.item import Item


class Stone(Item):
    def __init__(self):
        super().__init__('stone', 6)


class Iron(Item):
    def __init__(self):
        super().__init__('iron', 12)
