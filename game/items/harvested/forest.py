from game.items.item import Item


class Wood(Item):
    def __init__(self):
        super().__init__('wood', 5)


class Mushroom(Item):
    def __init__(self):
        super().__init__('mushroom', 4)


class Leaf(Item):
    def __init__(self):
        super().__init__('leaf', 2)
